import CoreGraphics
import Foundation

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
final class BrushTool: ColoringTool {
    let mode: ColoringMode = .freestyle
    var color: String
    var width: Double
    private var points: [Stroke.Point] = []

    init(color: String, width: Double) {
        self.color = color
        self.width = width
    }

    func began(at point: CGPoint, state: ColoringState) { points = [.init(x: point.x, y: point.y)] }
    func moved(to point: CGPoint, state: ColoringState) { points.append(.init(x: point.x, y: point.y)) }
    func ended(at point: CGPoint, state: ColoringState) {
        guard points.count > 1 else { return }
        state.dispatch(.stroke(Stroke(color: color, width: width, points: points)))
        points = []
    }
}

/// Fill, but only accepts the colour whose number matches the tapped region.
struct PaintByNumberTool: ColoringTool {
    let mode: ColoringMode = .paintByNumber
    let map: RegionMap
    let palette: Palette
    /// The number the child currently has selected in the tray.
    var selectedNumber: Int

    /// Returns true when the tap was correct; views use this to play the "yay"/"try again" sound.
    @discardableResult
    func tap(at point: CGPoint, state: ColoringState) -> Bool {
        guard let id = map.regionId(at: point), let entry = palette.entry(for: id) else { return false }
        guard entry.number == selectedNumber else { return false }
        state.dispatch(.fill(regionId: id, color: entry.color))
        return true
    }

    func began(at point: CGPoint, state: ColoringState) { tap(at: point, state: state) }
    func moved(to point: CGPoint, state: ColoringState) {}
    func ended(at point: CGPoint, state: ColoringState) {}

    func isComplete(_ state: ColoringState) -> Bool {
        palette.entries.allSatisfy { state.document.fills[$0.regionId] == $0.color }
    }
}
