import XCTest
@testable import SaudiColoring

final class FillToolTests: XCTestCase {
    // 5x1 map: red, red, outline, outline, blue.
    private let map = RegionMap(width: 5, height: 1, pixels: [0xFF0000, 0xFF0000, 0x000000, 0x000000, 0x0000FF])

    private func makeState() -> ColoringState {
        ColoringState(document: ColoringDocument(regionId: "riyadh", sceneId: "masmak-fort", mode: .fill))
    }

    func testTapFillsTheRegion() {
        let state = makeState()
        FillTool(map: map, color: "#00FF00").began(at: CGPoint(x: 4, y: 0), state: state)
        XCTAssertEqual(state.document.fills, [0x0000FF: "#00FF00"])
    }

    func testTapOnOutlineFillsNearestRegionWithinTolerance() {
        let state = makeState()
        FillTool(map: map, color: "#00FF00", tolerance: 1).began(at: CGPoint(x: 3, y: 0), state: state)
        XCTAssertEqual(state.document.fills, [0x0000FF: "#00FF00"])
    }

    func testTapOnOutlineWithoutToleranceDoesNothing() {
        let state = makeState()
        FillTool(map: map, color: "#00FF00").began(at: CGPoint(x: 3, y: 0), state: state)
        XCTAssertTrue(state.document.fills.isEmpty)
        XCTAssertFalse(state.canUndo)
    }

    func testSameColourTwiceIsOneUndoStep() {
        let state = makeState()
        let tool = FillTool(map: map, color: "#00FF00")
        tool.began(at: CGPoint(x: 0, y: 0), state: state)
        tool.began(at: CGPoint(x: 1, y: 0), state: state)
        state.dispatch(.undo)
        XCTAssertTrue(state.document.fills.isEmpty)
        XCTAssertFalse(state.canUndo)
    }

    func testPageIsCompleteWhenEveryRegionHasAColour() {
        let state = makeState()
        let tool = FillTool(map: map, color: "#00FF00")
        tool.began(at: CGPoint(x: 0, y: 0), state: state)
        XCTAssertFalse(FillTool.isComplete(regionIds: map.regionIds, document: state.document))
        tool.began(at: CGPoint(x: 4, y: 0), state: state)
        XCTAssertTrue(FillTool.isComplete(regionIds: map.regionIds, document: state.document))
    }

    func testModeAndCompletionAreNotUndoSteps() {
        let state = makeState()
        state.setMode(.paintByNumber)
        state.markCompleted(at: Date(timeIntervalSince1970: 1))
        state.markCompleted(at: Date(timeIntervalSince1970: 2))
        XCTAssertEqual(state.document.mode, .paintByNumber)
        XCTAssertEqual(state.document.completedAt, Date(timeIntervalSince1970: 1))
        XCTAssertFalse(state.canUndo)
    }

    func testNearestRegionPrefersTheCloserSide() {
        // 7x1: red, outline x5, blue. A tap at x=2 is closer to red.
        let wide = RegionMap(width: 7, height: 1, pixels: [0xFF0000, 0, 0, 0, 0, 0, 0x0000FF])
        XCTAssertEqual(wide.regionId(near: CGPoint(x: 2, y: 0), radius: 6), 0xFF0000)
        XCTAssertEqual(wide.regionId(near: CGPoint(x: 5, y: 0), radius: 6), 0x0000FF)
        XCTAssertNil(wide.regionId(near: CGPoint(x: 3, y: 0), radius: 2))
    }
}
