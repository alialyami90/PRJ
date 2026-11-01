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

    func testUndoAfterFinishingKeepsTheFinishedMark() {
        let state = makeState()
        state.dispatch(.fill(regionId: 1, color: "#FF0000"))
        state.markCompleted(at: Date(timeIntervalSince1970: 1))
        state.dispatch(.undo)
        XCTAssertTrue(state.document.fills.isEmpty)
        XCTAssertEqual(state.document.completedAt, Date(timeIntervalSince1970: 1))
        state.dispatch(.redo)
        XCTAssertEqual(state.document.fills[1], "#FF0000")
        XCTAssertEqual(state.document.completedAt, Date(timeIntervalSince1970: 1))
    }

    func testStartAgainClearsThePictureButKeepsTheFinishedMark() {
        let state = makeState()
        state.dispatch(.fill(regionId: 1, color: "#FF0000"))
        state.dispatch(.stroke(Stroke(color: "#00FF00", width: 4, points: [.init(x: 0, y: 0), .init(x: 1, y: 1)])))
        state.markCompleted(at: Date(timeIntervalSince1970: 1))
        state.dispatch(.reset)
        XCTAssertTrue(state.document.isEmpty)
        XCTAssertEqual(state.document.completedAt, Date(timeIntervalSince1970: 1))
        state.dispatch(.undo)
        XCTAssertEqual(state.document.fills[1], "#FF0000")
        XCTAssertEqual(state.document.completedAt, Date(timeIntervalSince1970: 1))
    }

    func testUndoKeepsTheModeTheChildIsIn() {
        let state = makeState()
        state.dispatch(.fill(regionId: 1, color: "#FF0000"))
        state.setMode(.freestyle)
        state.dispatch(.undo)
        XCTAssertEqual(state.document.mode, .freestyle)
    }
}
