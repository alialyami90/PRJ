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
    /// Set the first time the page is finished (every region coloured).
    var completedAt: Date?

    var isEmpty: Bool { fills.isEmpty && strokes.isEmpty }
}

enum ColoringMode: String, Codable, CaseIterable {
    case fill, freestyle

    /// Pages saved while Paint by Number existed (or any mode this build does not know) open in Fill.
    init(from decoder: Decoder) throws {
        self = ColoringMode(rawValue: try decoder.singleValueContainer().decode(String.self)) ?? .fill
    }
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
