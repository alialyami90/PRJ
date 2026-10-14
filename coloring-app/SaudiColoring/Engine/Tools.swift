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

    /// Every region has some colour. Pass the map's region ids, computed once per scene.
    static func isComplete(regionIds: Set<UInt32>, document: ColoringDocument) -> Bool {
        regionIds.allSatisfy { document.fills[$0] != nil }
    }
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

/// Fill, but only accepts the colour whose number matches the tapped region.
struct PaintByNumberTool: ColoringTool {
    enum Outcome: Equatable {
        /// The region took its colour.
        case correct
        /// The region needs a different number.
        case wrong(expected: Int)
        /// The region was already done, or the tap missed every region.
        case ignored
    }

    let mode: ColoringMode = .paintByNumber
    let map: RegionMap
    let palette: Palette
    /// The number the child currently has selected in the tray.
    var selectedNumber: Int
    /// Image pixels a tap may miss by and still hit the nearest region.
    var tolerance: Int = 0

    /// Views use the outcome to play the "yay" / "try again" feedback.
    @discardableResult
    func tap(at point: CGPoint, state: ColoringState) -> Outcome {
        guard let id = map.regionId(near: point, radius: tolerance), let entry = palette.entry(for: id) else { return .ignored }
        guard state.document.fills[id] != entry.color else { return .ignored }
        guard entry.number == selectedNumber else { return .wrong(expected: entry.number) }
        state.dispatch(.fill(regionId: id, color: entry.color))
        return .correct
    }

    func began(at point: CGPoint, state: ColoringState) { tap(at: point, state: state) }
    func moved(to point: CGPoint, state: ColoringState) {}
    func ended(at point: CGPoint, state: ColoringState) {}

    func isComplete(_ state: ColoringState) -> Bool {
        palette.entries.allSatisfy { isDone($0, state) }
    }

    /// Regions of `number` still waiting for their colour.
    func remaining(number: Int, _ state: ColoringState) -> [PaletteEntry] {
        palette.entries.filter { $0.number == number && !isDone($0, state) }
    }

    /// Numbers with nothing left to paint, for the tray's tick marks.
    func finishedNumbers(_ state: ColoringState) -> Set<Int> {
        var open = Set<Int>()
        for entry in palette.entries where !isDone(entry, state) { open.insert(entry.number) }
        return Set(palette.entries.map(\.number)).subtracting(open)
    }

    private func isDone(_ entry: PaletteEntry, _ state: ColoringState) -> Bool {
        state.document.fills[entry.regionId] == entry.color
    }
}
