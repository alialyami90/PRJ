import CoreGraphics
import Foundation
import ImageIO
import UniformTypeIdentifiers

/// Composites a coloring document into a bitmap the size of the scene:
/// fill layer (regions coloured via the map) → freestyle strokes → outline on top.
/// Used by the live canvas and, later, thumbnails and share export.
struct CanvasRenderer {
    let map: RegionMap
    /// Colour of regions the child has not filled yet.
    var paper: UInt32 = 0xFFFFFF
    /// Colour of the outline pixels (region id 0x000000 in the map).
    var ink: UInt32 = 0x000000
    /// Tint for unfilled regions Paint by Number is pointing at (the selected number's regions).
    var hint: UInt32 = 0xCFE6FF

    /// Per pixel: 0 for outline, otherwise 1 + the index of its region in `regionIds`.
    /// Precomputed once so a re-render is a table lookup per pixel.
    private let pixelSlots: [UInt16]
    private let regionIds: [UInt32]

    init(map: RegionMap) {
        self.map = map
        let ids = map.regionIds.sorted()
        precondition(ids.count < Int(UInt16.max), "too many regions for one scene")
        var slotFor: [UInt32: UInt16] = [RegionMap.outline: 0]
        for (i, id) in ids.enumerated() { slotFor[id] = UInt16(i + 1) }
        regionIds = ids
        pixelSlots = map.pixels.map { slotFor[$0] ?? 0 }
    }

    /// - Parameter highlight: regions to tint with `hint` while they are still unfilled.
    func render(_ document: ColoringDocument, highlight: Set<UInt32> = []) -> CGImage? {
        let w = map.width, h = map.height
        guard let ctx = CGContext(
            data: nil, width: w, height: h, bitsPerComponent: 8, bytesPerRow: 0,
            space: CGColorSpace(name: CGColorSpace.sRGB) ?? CGColorSpaceCreateDeviceRGB(),
            bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue
        ), let data = ctx.data else { return nil }

        var palette = [UInt32](repeating: paper, count: regionIds.count + 1)
        palette[0] = ink
        for (i, id) in regionIds.enumerated() {
            if let hex = document.fills[id], let rgb = SceneColor.rgb(fromHex: hex) {
                palette[i + 1] = rgb
            } else if highlight.contains(id) {
                palette[i + 1] = hint
            }
        }

        let rowBytes = ctx.bytesPerRow
        let raw = data.bindMemory(to: UInt8.self, capacity: rowBytes * h)
        pixelSlots.withUnsafeBufferPointer { slots in
            palette.withUnsafeBufferPointer { lut in
                for y in 0..<h {
                    let row = raw + y * rowBytes
                    for x in 0..<w {
                        let c = lut[Int(slots[y * w + x])]
                        let p = row + x * 4
                        p[0] = UInt8(truncatingIfNeeded: c >> 16)
                        p[1] = UInt8(truncatingIfNeeded: c >> 8)
                        p[2] = UInt8(truncatingIfNeeded: c)
                        p[3] = 0xFF
                    }
                }
            }
        }

        if !document.strokes.isEmpty {
            drawStrokes(document.strokes, in: ctx, height: h)
            stampOutline(into: raw, rowBytes: rowBytes)
        }
        return ctx.makeImage()
    }

    /// Strokes are in image space with a top-left origin, like touches.
    private func drawStrokes(_ strokes: [Stroke], in ctx: CGContext, height: Int) {
        ctx.saveGState()
        ctx.translateBy(x: 0, y: CGFloat(height))
        ctx.scaleBy(x: 1, y: -1)
        ctx.setLineCap(.round)
        ctx.setLineJoin(.round)
        for stroke in strokes {
            guard let first = stroke.points.first, let rgb = SceneColor.rgb(fromHex: stroke.color) else { continue }
            ctx.setStrokeColor(red: CGFloat(rgb >> 16 & 0xFF) / 255, green: CGFloat(rgb >> 8 & 0xFF) / 255,
                               blue: CGFloat(rgb & 0xFF) / 255, alpha: 1)
            ctx.setLineWidth(stroke.width)
            ctx.beginPath()
            ctx.move(to: CGPoint(x: first.x, y: first.y))
            for point in stroke.points.dropFirst() { ctx.addLine(to: CGPoint(x: point.x, y: point.y)) }
            ctx.strokePath()
        }
        ctx.restoreGState()
    }

    /// Puts the outline back on top of any paint that crossed it.
    private func stampOutline(into raw: UnsafeMutablePointer<UInt8>, rowBytes: Int) {
        let w = map.width
        pixelSlots.withUnsafeBufferPointer { slots in
            for y in 0..<map.height {
                let row = raw + y * rowBytes
                for x in 0..<w where slots[y * w + x] == 0 {
                    let p = row + x * 4
                    p[0] = UInt8(truncatingIfNeeded: ink >> 16)
                    p[1] = UInt8(truncatingIfNeeded: ink >> 8)
                    p[2] = UInt8(truncatingIfNeeded: ink)
                }
            }
        }
    }

    /// A small PNG of a rendered page for the gallery, at most `maxWidth` pixels wide.
    static func thumbnailPNG(of image: CGImage, maxWidth: Int = 512) -> Data? {
        let scale = min(1, Double(maxWidth) / Double(image.width))
        let w = max(1, Int(Double(image.width) * scale)), h = max(1, Int(Double(image.height) * scale))
        guard let ctx = CGContext(
            data: nil, width: w, height: h, bitsPerComponent: 8, bytesPerRow: 0,
            space: CGColorSpace(name: CGColorSpace.sRGB) ?? CGColorSpaceCreateDeviceRGB(),
            bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue
        ) else { return nil }
        ctx.interpolationQuality = .high
        ctx.draw(image, in: CGRect(x: 0, y: 0, width: w, height: h))
        guard let small = ctx.makeImage() else { return nil }
        let data = NSMutableData()
        guard let dest = CGImageDestinationCreateWithData(data as CFMutableData, UTType.png.identifier as CFString, 1, nil) else { return nil }
        CGImageDestinationAddImage(dest, small, nil)
        guard CGImageDestinationFinalize(dest) else { return nil }
        return data as Data
    }
}
