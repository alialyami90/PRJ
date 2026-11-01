import CoreGraphics
import Foundation
import Observation

/// A coloring mode is a strategy that turns touches into ColoringActions.
protocol ColoringTool {
    var mode: ColoringMode { get }
    func began(at point: CGPoint, state: ColoringState)
    func moved(to point: CGPoint, state: ColoringState)
    func ended(at point: CGPoint, state: ColoringState)
}

/// Tap a region to fill it with the selected colour.
struct FillTool: ColoringTool {
    let mode: ColoringMode = .fill
    let map: RegionMap
    var color: String
    /// Image pixels a tap may miss by (e.g. landing on an outline) and still fill the nearest region.
    var tolerance: Int = 0

    func began(at point: CGPoint, state: ColoringState) {
        guard let id = map.regionId(near: point, radius: tolerance) else { return }
        // Re-tapping a region with the colour it already has is not a new undo step.
        guard state.document.fills[id] != color else { return }
        state.dispatch(.fill(regionId: id, color: color))
    }
    func moved(to point: CGPoint, state: ColoringState) {}
    func ended(at point: CGPoint, state: ColoringState) {}
}

/// Freehand brush; accumulates points and commits one Stroke on touch end.
/// Observable so the canvas can draw the stroke in progress before it is committed.
@Observable
final class BrushTool: ColoringTool {
    let mode: ColoringMode = .freestyle
    var color: String
    /// Line width in image pixels.
    var width: Double
    private(set) var points: [Stroke.Point] = []

    init(color: String, width: Double) {
        self.color = color
        self.width = width
    }

    func began(at point: CGPoint, state: ColoringState) { points = [.init(x: point.x, y: point.y)] }
    func moved(to point: CGPoint, state: ColoringState) {
        guard !points.isEmpty else { return }
        points.append(.init(x: point.x, y: point.y))
    }
    func ended(at point: CGPoint, state: ColoringState) {
        guard let first = points.first else { return }
        // A tap without movement is a dot: a zero-length line with round caps.
        let stroke = points.count > 1 ? points : [first, first]
        state.dispatch(.stroke(Stroke(color: color, width: width, points: stroke)))
        points = []
    }
    /// A second finger landed (pinch/pan): drop the stroke in progress.
    func cancel() { points = [] }
}
