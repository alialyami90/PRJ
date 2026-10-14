import XCTest
@testable import SaudiColoring

final class ColoringStateTests: XCTestCase {
    private func makeState() -> ColoringState {
        ColoringState(document: ColoringDocument(regionId: "riyadh", sceneId: "masmak-fort", mode: .fill))
    }

    func testFillThenUndoRedo() {
        let state = makeState()
        state.dispatch(.fill(regionId: 1, color: "#FF0000"))
        XCTAssertEqual(state.document.fills[1], "#FF0000")
        state.dispatch(.undo)
        XCTAssertNil(state.document.fills[1])
        state.dispatch(.redo)
        XCTAssertEqual(state.document.fills[1], "#FF0000")
    }

    func testNewActionClearsRedo() {
        let state = makeState()
        state.dispatch(.fill(regionId: 1, color: "#FF0000"))
        state.dispatch(.undo)
        state.dispatch(.fill(regionId: 2, color: "#00FF00"))
        XCTAssertFalse(state.canRedo)
    }

    func testPaintByNumberRejectsWrongNumber() {
        let map = RegionMap(width: 1, height: 1, pixels: [0xABCDEF])
        let palette = Palette(entries: [PaletteEntry(regionId: 0xABCDEF, number: 2, color: "#123456")])
        let state = makeState()
        var tool = PaintByNumberTool(map: map, palette: palette, selectedNumber: 1)
        XCTAssertEqual(tool.tap(at: .zero, state: state), .wrong(expected: 2))
        XCTAssertTrue(state.document.fills.isEmpty)
        tool.selectedNumber = 2
        XCTAssertEqual(tool.tap(at: .zero, state: state), .correct)
        XCTAssertTrue(tool.isComplete(state))
        // A finished region is not a new undo step.
        XCTAssertEqual(tool.tap(at: .zero, state: state), .ignored)
        state.dispatch(.undo)
        XCTAssertTrue(state.document.fills.isEmpty)
    }

    func testPaintByNumberTracksFinishedNumbers() {
        // red(1) | outline | blue(2) | green(1)
        let map = RegionMap(width: 4, height: 1, pixels: [0xFF0000, 0, 0x0000FF, 0x00FF00])
        let palette = Palette(entries: [
            PaletteEntry(regionId: 0xFF0000, number: 1, color: "#111111"),
            PaletteEntry(regionId: 0x0000FF, number: 2, color: "#222222"),
            PaletteEntry(regionId: 0x00FF00, number: 1, color: "#111111"),
        ])
        let state = makeState()
        let tool = PaintByNumberTool(map: map, palette: palette, selectedNumber: 1, tolerance: 1)
        // A tap on the outline lands on the nearest region.
        XCTAssertEqual(tool.tap(at: CGPoint(x: 1, y: 0), state: state), .correct)
        XCTAssertEqual(tool.remaining(number: 1, state).map(\.regionId), [0x00FF00])
        XCTAssertEqual(tool.finishedNumbers(state), [])
        tool.tap(at: CGPoint(x: 3, y: 0), state: state)
        XCTAssertEqual(tool.finishedNumbers(state), [1])
        XCTAssertFalse(tool.isComplete(state))
    }

    func testBrushCommitsOneStrokeAndTurnsATapIntoADot() {
        let state = makeState()
        let brush = BrushTool(color: "#FF0000", width: 20)
        brush.began(at: CGPoint(x: 1, y: 1), state: state)
        brush.moved(to: CGPoint(x: 5, y: 5), state: state)
        XCTAssertEqual(brush.points.count, 2)
        brush.ended(at: CGPoint(x: 5, y: 5), state: state)
        XCTAssertEqual(state.document.strokes.count, 1)
        XCTAssertTrue(brush.points.isEmpty)

        brush.began(at: CGPoint(x: 9, y: 9), state: state)
        brush.ended(at: CGPoint(x: 9, y: 9), state: state)
        XCTAssertEqual(state.document.strokes.last?.points.count, 2)

        brush.began(at: CGPoint(x: 1, y: 1), state: state)
        brush.cancel()
        brush.ended(at: CGPoint(x: 1, y: 1), state: state)
        XCTAssertEqual(state.document.strokes.count, 2)
    }
}
