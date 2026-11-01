import XCTest
@testable import SaudiColoring

final class PageProgressTests: XCTestCase {
    private let red: UInt32 = 0xFF0000, blue: UInt32 = 0x0000FF, green: UInt32 = 0x00FF00

    func testABlankPageIsNotFinishedAndPointsAtTheBiggestShapesFirst() {
        let progress = PageProgress(areas: [red: 10, blue: 300, green: 50], fills: [:])
        XCTAssertEqual(progress.covered, 0)
        XCTAssertFalse(progress.isFinished)
        XCTAssertEqual(progress.whiteShapes, [blue, green, red])
    }

    func testEveryShapeColouredIsFinished() {
        let progress = PageProgress(areas: [red: 10, blue: 300], fills: [red: "#111111", blue: "#222222"])
        XCTAssertEqual(progress.covered, 1)
        XCTAssertTrue(progress.isFinished)
        XCTAssertTrue(progress.whiteShapes.isEmpty)
    }

    func testSliversLeftWhiteStillFinishThePage() {
        // One big shape of 900 pixels and 100 slivers of 1 pixel: colouring the big one leaves 10% white,
        // in patches far too small to notice.
        var areas: [UInt32: Int] = [red: 900]
        for id in 1...100 { areas[UInt32(id)] = 1 }
        let progress = PageProgress(areas: areas, fills: [red: "#111111"])
        XCTAssertEqual(progress.covered, 0.9, accuracy: 1e-9)
        XCTAssertTrue(progress.isFinished)
        XCTAssertEqual(progress.whiteShapes.count, 100)
    }

    func testTooMuchWhiteOverallIsNotFinished() {
        var areas: [UInt32: Int] = [red: 850]
        for id in 1...150 { areas[UInt32(id)] = 1 }
        XCTAssertFalse(PageProgress(areas: areas, fills: [red: "#111111"]).isFinished)
    }

    func testOneBigWhiteShapeIsNotFinished() {
        // Only 5% of the page is white, but all of it in one shape that stands out.
        let progress = PageProgress(areas: [red: 950, blue: 50], fills: [red: "#111111"])
        XCTAssertFalse(progress.isFinished)
        XCTAssertEqual(progress.whiteShapes, [blue])
    }

    func testBrushPaintCountsAsColour() {
        let areas: [UInt32: Int] = [red: 900, blue: 100]
        XCTAssertFalse(PageProgress(areas: areas, fills: [red: "#111111"], painted: [blue: 60]).isFinished)
        let painted = PageProgress(areas: areas, fills: [red: "#111111"], painted: [blue: 99])
        XCTAssertTrue(painted.isFinished)
        XCTAssertTrue(painted.whiteShapes.isEmpty)
        // Paint is counted up to the shape's own size.
        XCTAssertEqual(PageProgress(areas: [blue: 100], fills: [:], painted: [blue: 500]).covered, 1)
    }

    func testAShapeHalfPaintedIsStillAWhiteShape() {
        let progress = PageProgress(areas: [red: 100, blue: 100], fills: [:], painted: [red: 40, blue: 60])
        XCTAssertEqual(progress.whiteShapes, [red])
        XCTAssertEqual(progress.covered, 0.5, accuracy: 1e-9)
    }

    func testAPageWithNoShapesIsNeverFinished() {
        XCTAssertFalse(PageProgress(areas: [:], fills: [:]).isFinished)
    }
}
