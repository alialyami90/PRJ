import CoreGraphics
import Foundation

/// Where Paint by Number writes a region's number: the point deepest inside the region.
struct RegionLabel: Equatable {
    /// Image-space centre for the number.
    let point: CGPoint
    /// Distance in image pixels from `point` to the region's edge; bounds the font size.
    let radius: Double
}

extension RegionMap {
    /// For every region, the pixel farthest from its edge (the outline, paper, another region or the image border).
    /// A two-pass chamfer distance transform, so one pass over the map whatever the region count.
    /// Concave shapes (a crescent, an L) get a point inside them, unlike a centroid.
    func labels() -> [UInt32: RegionLabel] {
        let w = width, h = height
        guard w > 0, h > 0 else { return [:] }
        let straight: Int32 = 3, diagonal: Int32 = 4 // 3-4 chamfer: distance ≈ value / 3
        var dist = [Int32](repeating: 0, count: w * h)

        pixels.withUnsafeBufferPointer { id in
            dist.withUnsafeMutableBufferPointer { buffer in
                let d = buffer // the subscript setter is nonmutating; a copy keeps the helper below non-inout
                // A neighbour outside the image or in another region counts as edge (distance 0).
                @inline(__always) func at(_ x: Int, _ y: Int, _ own: UInt32) -> Int32 {
                    guard x >= 0, y >= 0, x < w, y < h else { return 0 }
                    let i = y * w + x
                    return id[i] == own ? d[i] : 0
                }
                for y in 0..<h {
                    for x in 0..<w {
                        let i = y * w + x
                        let own = id[i]
                        guard Self.isRegion(own) else { continue }
                        d[i] = min(min(at(x - 1, y, own) + straight, at(x, y - 1, own) + straight),
                                   min(at(x - 1, y - 1, own) + diagonal, at(x + 1, y - 1, own) + diagonal))
                    }
                }
                for y in stride(from: h - 1, through: 0, by: -1) {
                    for x in stride(from: w - 1, through: 0, by: -1) {
                        let i = y * w + x
                        let own = id[i]
                        guard Self.isRegion(own) else { continue }
                        d[i] = min(d[i], min(min(at(x + 1, y, own) + straight, at(x, y + 1, own) + straight),
                                             min(at(x + 1, y + 1, own) + diagonal, at(x - 1, y + 1, own) + diagonal)))
                    }
                }
            }
        }

        var best: [UInt32: (index: Int, value: Int32)] = [:]
        for i in 0..<(w * h) {
            let own = pixels[i]
            guard Self.isRegion(own) else { continue }
            if dist[i] > best[own]?.value ?? -1 { best[own] = (i, dist[i]) }
        }
        return best.mapValues { b in
            RegionLabel(point: CGPoint(x: Double(b.index % w) + 0.5, y: Double(b.index / w) + 0.5),
                        radius: Double(b.value) / Double(straight))
        }
    }
}
