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
        XCTAssertFalse(tool.tap(at: .zero, state: state))
        tool.selectedNumber = 2
        XCTAssertTrue(tool.tap(at: .zero, state: state))
        XCTAssertTrue(tool.isComplete(state))
    }
}
