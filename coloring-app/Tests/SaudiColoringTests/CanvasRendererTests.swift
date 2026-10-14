import CoreGraphics
import ImageIO
import XCTest
@testable import SaudiColoring

final class CanvasRendererTests: XCTestCase {
    // 3x2 map: red region | outline | blue region.
    private let map = RegionMap(width: 3, height: 2, pixels: [
        0xFF0000, 0x000000, 0x0000FF,
        0xFF0000, 0x000000, 0x0000FF,
    ])

    private func document() -> ColoringDocument {
        ColoringDocument(regionId: "riyadh", sceneId: "masmak-fort", mode: .fill)
    }

    func testUnfilledRegionsArePaperAndOutlineIsInk() throws {
        let pixels = try XCTUnwrap(CanvasRenderer(map: map).render(document())).rgbPixels()
        XCTAssertEqual(pixels, [
            0xFFFFFF, 0x000000, 0xFFFFFF,
            0xFFFFFF, 0x000000, 0xFFFFFF,
        ])
    }

    func testPaperStaysWhite() throws {
        let map = RegionMap(width: 3, height: 1, pixels: [0xFF0000, RegionMap.paper, 0x000000])
        var doc = document()
        doc.fills[0xFF0000] = "#12AB34"
        doc.fills[RegionMap.paper] = "#123456" // never a region; ignored
        let pixels = try XCTUnwrap(CanvasRenderer(map: map).render(doc, highlight: [RegionMap.paper])).rgbPixels()
        XCTAssertEqual(pixels, [0x12AB34, 0xFFFFFF, 0x000000])
    }

    func testFilledRegionUsesDocumentColour() throws {
        var doc = document()
        doc.fills[0x0000FF] = "#12AB34"
        let pixels = try XCTUnwrap(CanvasRenderer(map: map).render(doc)).rgbPixels()
        XCTAssertEqual(pixels, [
            0xFFFFFF, 0x000000, 0x12AB34,
            0xFFFFFF, 0x000000, 0x12AB34,
        ])
    }

    func testFillsForUnknownRegionsAndBadColoursAreIgnored() throws {
        var doc = document()
        doc.fills[0x00FF00] = "#123456"   // not in this map
        doc.fills[0xFF0000] = "not a colour"
        let pixels = try XCTUnwrap(CanvasRenderer(map: map).render(doc)).rgbPixels()
        XCTAssertEqual(pixels[0], 0xFFFFFF)
    }

    func testOutlineStaysOnTopOfStrokes() throws {
        var doc = document()
        // A thick stroke across the whole image.
        doc.strokes = [Stroke(color: "#00FF00", width: 10, points: [.init(x: -5, y: 1), .init(x: 8, y: 1)])]
        let pixels = try XCTUnwrap(CanvasRenderer(map: map).render(doc)).rgbPixels()
        XCTAssertEqual(pixels, [
            0x00FF00, 0x000000, 0x00FF00,
            0x00FF00, 0x000000, 0x00FF00,
        ])
    }

    func testHighlightTintsOnlyUnfilledRegions() throws {
        var doc = document()
        doc.fills[0x0000FF] = "#12AB34"
        let renderer = CanvasRenderer(map: map)
        let pixels = try XCTUnwrap(renderer.render(doc, highlight: [0xFF0000, 0x0000FF])).rgbPixels()
        XCTAssertEqual(pixels, [
            renderer.hint, 0x000000, 0x12AB34,
            renderer.hint, 0x000000, 0x12AB34,
        ])
    }

    func testThumbnailIsAPNGAtMostTheRequestedWidth() throws {
        let assets = try SceneAssets.load(regionId: "riyadh", sceneId: "masmak-fort")
        let image = try XCTUnwrap(CanvasRenderer(map: assets.map).render(document()))
        let png = try XCTUnwrap(CanvasRenderer.thumbnailPNG(of: image, maxWidth: 256))
        XCTAssertEqual(Array(png.prefix(4)), [0x89, 0x50, 0x4E, 0x47])
        let source = try XCTUnwrap(CGImageSourceCreateWithData(png as CFData, nil))
        let thumb = try XCTUnwrap(CGImageSourceCreateImageAtIndex(source, 0, nil))
        XCTAssertEqual(thumb.width, 256)
        XCTAssertEqual(thumb.height, 192)
    }

    func testRendersTheSampleSceneAtFullSize() throws {
        let assets = try SceneAssets.load(regionId: "riyadh", sceneId: "masmak-fort")
        let image = try XCTUnwrap(CanvasRenderer(map: assets.map).render(document()))
        XCTAssertEqual(image.width, assets.map.width)
        XCTAssertEqual(image.height, assets.map.height)
    }
}

extension CGImage {
    /// Pixels as packed 0xRRGGBB, row-major from the top-left.
    func rgbPixels() -> [UInt32] {
        let ctx = CGContext(
            data: nil, width: width, height: height, bitsPerComponent: 8, bytesPerRow: 0,
            space: CGColorSpace(name: CGColorSpace.sRGB)!,
            bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue
        )!
        ctx.draw(self, in: CGRect(x: 0, y: 0, width: width, height: height))
        let raw = ctx.data!.bindMemory(to: UInt8.self, capacity: ctx.bytesPerRow * height)
        var out: [UInt32] = []
        for y in 0..<height {
            for x in 0..<width {
                let p = raw + y * ctx.bytesPerRow + x * 4
                out.append(UInt32(p[0]) << 16 | UInt32(p[1]) << 8 | UInt32(p[2]))
            }
        }
        return out
    }
}
