import CoreGraphics
import Foundation
import ImageIO
import UniformTypeIdentifiers

/// Composites a coloring document into a bitmap the size of the scene:
/// fill layer (regions coloured via the map) → freestyle strokes → outline on top.
/// Used by the live canvas, the gallery thumbnails and, later, share export.
struct CanvasRenderer {
    let map: RegionMap
    /// Colour of regions the child has not filled yet.
    var paper: UInt32 = 0xFFFFFF
    /// Colour of the outline pixels (region id 0x000000 in the map).
    var ink: UInt32 = 0x000000

    /// Per pixel: 0 for outline, 1 + the index of its region in `regionIds`, or 1 + regionIds.count for paper.
    /// Precomputed once so a re-render is a table lookup per pixel.
    private let pixelSlots: [UInt16]
    private let regionIds: [UInt32]
    /// Pixels per region, for PageProgress.
    let regionAreas: [UInt32: Int]

    /// A rendered page and how much of each unfilled region the brush has coloured.
    struct Rendered {
        let image: CGImage?
        /// Region id -> pixels that strokes turned from paper to a colour, for regions without a fill.
        let painted: [UInt32: Int]
    }

    init(map: RegionMap) {
        self.map = map
        let ids = map.regionIds.sorted()
        precondition(ids.count < Int(UInt16.max), "too many regions for one scene")
        var slotFor: [UInt32: UInt16] = [RegionMap.outline: 0, RegionMap.paper: UInt16(ids.count + 1)]
        for (i, id) in ids.enumerated() { slotFor[id] = UInt16(i + 1) }
        regionIds = ids
        let slots = map.pixels.map { slotFor[$0] ?? 0 }
        pixelSlots = slots
        var counts = [Int](repeating: 0, count: ids.count + 2)
        for slot in slots { counts[Int(slot)] += 1 }
        var areas: [UInt32: Int] = [:]
        for (i, id) in ids.enumerated() { areas[id] = counts[i + 1] }
        regionAreas = areas
    }

    func render(_ document: ColoringDocument) -> CGImage? {
        renderPage(document).image
    }

    func renderPage(_ document: ColoringDocument) -> Rendered {
        let w = map.width, h = map.height
        guard let ctx = CGContext(
            data: nil, width: w, height: h, bitsPerComponent: 8, bytesPerRow: 0,
            space: CGColorSpace(name: CGColorSpace.sRGB) ?? CGColorSpaceCreateDeviceRGB(),
            bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue
        ), let data = ctx.data else { return Rendered(image: nil, painted: [:]) }

        var palette = [UInt32](repeating: paper, count: regionIds.count + 2) // the last slot is paper
        palette[0] = ink
        for (i, id) in regionIds.enumerated() {
            if let hex = document.fills[id], let rgb = SceneColor.rgb(fromHex: hex) {
                palette[i + 1] = rgb
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

        var painted: [UInt32: Int] = [:]
        if !document.strokes.isEmpty {
            drawStrokes(document.strokes, in: ctx, height: h)
            stampOutline(into: raw, rowBytes: rowBytes)
            painted = paintedPixels(in: raw, rowBytes: rowBytes, palette: palette)
        }
        return Rendered(image: ctx.makeImage(), painted: painted)
    }

    /// Pixels of each unfilled region that are no longer paper after the strokes were drawn.
    private func paintedPixels(in raw: UnsafeMutablePointer<UInt8>, rowBytes: Int, palette: [UInt32]) -> [UInt32: Int] {
        let w = map.width, count = regionIds.count
        // Only regions still drawn as paper can gain colour from the brush.
        let unfilled = palette.indices.map { $0 >= 1 && $0 <= count && palette[$0] == paper }
        var counts = [Int](repeating: 0, count: count + 2)
        pixelSlots.withUnsafeBufferPointer { slots in
            for y in 0..<map.height {
                let row = raw + y * rowBytes
                for x in 0..<w {
                    let slot = Int(slots[y * w + x])
                    guard unfilled[slot] else { continue }
                    let p = row + x * 4
                    let c = UInt32(p[0]) << 16 | UInt32(p[1]) << 8 | UInt32(p[2])
                    if c != paper { counts[slot] += 1 }
                }
            }
        }
        var painted: [UInt32: Int] = [:]
        for (i, id) in regionIds.enumerated() where counts[i + 1] > 0 { painted[id] = counts[i + 1] }
        return painted
    }

    /// The given regions in `color` on a clear image the size of the page, for the finishing hint.
    func highlight(_ ids: Set<UInt32>, color: UInt32) -> CGImage? {
        let w = map.width, h = map.height
        guard let ctx = CGContext(
            data: nil, width: w, height: h, bitsPerComponent: 8, bytesPerRow: 0,
            space: CGColorSpace(name: CGColorSpace.sRGB) ?? CGColorSpaceCreateDeviceRGB(),
            bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue
        ), let data = ctx.data else { return nil }
        var marked = [Bool](repeating: false, count: regionIds.count + 2)
        for (i, id) in regionIds.enumerated() where ids.contains(id) { marked[i + 1] = true }
        let r = UInt8(truncatingIfNeeded: color >> 16), g = UInt8(truncatingIfNeeded: color >> 8)
        let b = UInt8(truncatingIfNeeded: color)
        let rowBytes = ctx.bytesPerRow
        let raw = data.bindMemory(to: UInt8.self, capacity: rowBytes * h)
        pixelSlots.withUnsafeBufferPointer { slots in
            for y in 0..<h {
                let row = raw + y * rowBytes
                for x in 0..<w {
                    let p = row + x * 4
                    if marked[Int(slots[y * w + x])] {
                        p[0] = r; p[1] = g; p[2] = b; p[3] = 0xFF
                    } else {
                        p[0] = 0; p[1] = 0; p[2] = 0; p[3] = 0
                    }
                }
            }
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
