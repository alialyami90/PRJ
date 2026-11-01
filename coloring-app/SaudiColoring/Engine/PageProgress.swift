import Foundation

/// How much of a page has colour, and whether that counts as finished.
///
/// Pages have 60 to 311 shapes, many of them slivers, and a child decides a picture is done long
/// before every one has paint. So a page is finished when nearly all of its colourable area has colour
/// and no single white patch is big enough to stand out. The same rule holds in Fill and in Paint.
struct PageProgress: Equatable {
    /// Share of the page's colourable area that has colour, 0...1.
    let covered: Double
    let isFinished: Bool
    /// Shapes that are still mostly white, biggest first: where the finishing hint points.
    let whiteShapes: [UInt32]

    /// At most this share of the colourable area may still be white.
    static let maxWhite = 0.10
    /// No one white patch may be bigger than this share of the colourable area (a sky, a wall, a robe).
    static let maxWhitePatch = 0.015
    /// A shape with at least this share of itself still white counts as a white shape.
    static let whiteShapeShare = 0.5

    /// - Parameters:
    ///   - areas: pixels per region (`CanvasRenderer.regionAreas`).
    ///   - fills: the document's fills; a filled region is coloured all over.
    ///   - painted: pixels per unfilled region that brush strokes have coloured (`CanvasRenderer.Rendered.painted`).
    init(areas: [UInt32: Int], fills: [UInt32: String], painted: [UInt32: Int] = [:]) {
        let total = areas.values.reduce(0, +)
        guard total > 0 else {
            covered = 0
            isFinished = false
            whiteShapes = []
            return
        }
        var white = 0
        var biggestPatch = 0
        var shapes: [(id: UInt32, area: Int)] = []
        for (id, area) in areas where area > 0 {
            let coloured = fills[id] != nil ? area : min(area, painted[id] ?? 0)
            let left = area - coloured
            white += left
            biggestPatch = max(biggestPatch, left)
            if Double(left) >= Double(area) * Self.whiteShapeShare { shapes.append((id, area)) }
        }
        covered = 1 - Double(white) / Double(total)
        isFinished = Double(white) <= Self.maxWhite * Double(total)
            && Double(biggestPatch) <= Self.maxWhitePatch * Double(total)
        whiteShapes = shapes
            .sorted { $0.area != $1.area ? $0.area > $1.area : $0.id < $1.id }
            .map(\.id)
    }
}
