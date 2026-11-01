import CoreGraphics
import Foundation

/// An index map decoded from a scene's regions.png: every fillable region is a
/// unique flat colour. Looking up the region under a touch is one array read.
struct RegionMap {
    let width: Int
    let height: Int
    /// 0xRRGGBB per pixel, row-major. 0x000000 (outline) and 0xFFFFFF (paper) are not regions.
    let pixels: [UInt32]

    static let outline: UInt32 = 0x000000
    /// White the child cannot colour: shapes too small for a finger, and the shine on a pupil that the
    /// line art leaves open to the face (Scripts/import_illustration.py). Always drawn as paper.
    static let paper: UInt32 = 0xFFFFFF

    init(width: Int, height: Int, pixels: [UInt32]) {
        precondition(pixels.count == width * height)
        self.width = width
        self.height = height
        self.pixels = pixels
    }

    init?(cgImage: CGImage) {
        let w = cgImage.width, h = cgImage.height
        // Let CoreGraphics own the backing store; a pointer into a Swift array must not outlive the call.
        guard let ctx = CGContext(
            data: nil, width: w, height: h, bitsPerComponent: 8, bytesPerRow: 0,
            space: CGColorSpace(name: CGColorSpace.sRGB) ?? CGColorSpaceCreateDeviceRGB(),
            bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue
        ), let data = ctx.data else { return nil }
        // Region ids are exact RGB values: never interpolate.
        ctx.interpolationQuality = .none
        ctx.draw(cgImage, in: CGRect(x: 0, y: 0, width: w, height: h))
        let rowBytes = ctx.bytesPerRow
        let raw = data.bindMemory(to: UInt8.self, capacity: rowBytes * h)
        var px = [UInt32](repeating: 0, count: w * h)
        px.withUnsafeMutableBufferPointer { out in
            for y in 0..<h {
                let row = raw + y * rowBytes
                for x in 0..<w {
                    let p = row + x * 4
                    out[y * w + x] = UInt32(p[0]) << 16 | UInt32(p[1]) << 8 | UInt32(p[2])
                }
            }
        }
        self.init(width: w, height: h, pixels: px)
    }

    /// Region id at an image-space point, or nil when outside the image, on the outline or on paper.
    func regionId(at point: CGPoint) -> UInt32? {
        guard point.x >= 0, point.y >= 0 else { return nil }
        let x = Int(point.x), y = Int(point.y)
        guard x < width, y < height else { return nil }
        let id = pixels[y * width + x]
        return Self.isRegion(id) ? id : nil
    }

    /// False for the outline and paper.
    static func isRegion(_ id: UInt32) -> Bool { id != outline && id != paper }

    /// The region at `point`, or, when the point is on the outline or paper, the nearest region within
    /// `radius` pixels. Kids' taps land on the lines all the time.
    func regionId(near point: CGPoint, radius: Int) -> UInt32? {
        if let id = regionId(at: point) { return id }
        guard radius > 0, point.x >= 0, point.y >= 0 else { return nil }
        let cx = Int(point.x), cy = Int(point.y)
        guard cx < width, cy < height else { return nil }
        var best: (distance: Int, id: UInt32)?
        for y in max(0, cy - radius)...min(height - 1, cy + radius) {
            for x in max(0, cx - radius)...min(width - 1, cx + radius) {
                let id = pixels[y * width + x]
                guard Self.isRegion(id) else { continue }
                let d = (x - cx) * (x - cx) + (y - cy) * (y - cy)
                if d <= radius * radius, d < (best?.distance ?? .max) { best = (d, id) }
            }
        }
        return best?.id
    }

    /// All distinct region ids.
    var regionIds: Set<UInt32> {
        Set(pixels).subtracting([Self.outline, Self.paper])
    }
}
