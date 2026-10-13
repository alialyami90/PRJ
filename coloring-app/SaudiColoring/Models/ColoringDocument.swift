import Foundation

/// Everything needed to restore a child's progress on one scene. Persisted as JSON.
struct ColoringDocument: Codable {
    var regionId: String
    var sceneId: String
    var mode: ColoringMode
    /// regionId (from regions.png) -> "#RRGGBB"
    var fills: [UInt32: String] = [:]
    var strokes: [Stroke] = []
    var updatedAt: Date = .now

    var isEmpty: Bool { fills.isEmpty && strokes.isEmpty }
}

enum ColoringMode: String, Codable, CaseIterable {
    case fill, freestyle, paintByNumber
}

struct Stroke: Codable, Hashable {
    struct Point: Codable, Hashable {
        var x: Double
        var y: Double
        var pressure: Double = 1
    }
    var color: String
    var width: Double
    var points: [Point]
}
