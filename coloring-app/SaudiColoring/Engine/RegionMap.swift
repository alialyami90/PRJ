import CoreGraphics
import Foundation

/// An index map decoded from a scene's regions.png: every fillable region is a
/// unique flat colour. Looking up the region under a touch is one array read.
struct RegionMap {
    let width: Int
    let height: Int
    /// 0xRRGGBB per pixel, row-major. 0x000000 is reserved for "outline / not fillable".
    let pixels: [UInt32]

    static let outline: UInt32 = 0x000000

    init(width: Int, height: Int, pixels: [UInt32]) {
        precondition(pixels.count == width * height)
        self.width = width
        self.height = height
        self.pixels = pixels
    }

    init?(cgImage: CGImage) {
        let w = cgImage.width, h = cgImage.height
        var raw = [UInt8](repeating: 0, count: w * h * 4)
        guard let ctx = CGContext(
            data: &raw, width: w, height: h, bitsPerComponent: 8, bytesPerRow: w * 4,
            space: CGColorSpaceCreateDeviceRGB(),
            bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue
        ) else { return nil }
        ctx.draw(cgImage, in: CGRect(x: 0, y: 0, width: w, height: h))
        var px = [UInt32](repeating: 0, count: w * h)
        for i in 0..<(w * h) {
            px[i] = UInt32(raw[i * 4]) << 16 | UInt32(raw[i * 4 + 1]) << 8 | UInt32(raw[i * 4 + 2])
        }
        self.init(width: w, height: h, pixels: px)
    }

    /// Region id at an image-space point, or nil when outside the image or on the outline.
    func regionId(at point: CGPoint) -> UInt32? {
        let x = Int(point.x), y = Int(point.y)
        guard x >= 0, y >= 0, x < width, y < height else { return nil }
        let id = pixels[y * width + x]
        return id == Self.outline ? nil : id
    }

    /// All distinct region ids, for building masks and PBN completion checks.
    var regionIds: Set<UInt32> {
        Set(pixels).subtracting([Self.outline])
    }
}
