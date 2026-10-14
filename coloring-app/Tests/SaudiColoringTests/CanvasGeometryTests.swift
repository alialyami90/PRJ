import XCTest
@testable import SaudiColoring

final class CanvasGeometryTests: XCTestCase {
    // A 4:3 scene in a wide view letterboxes left and right.
    private let geometry = CanvasGeometry(imageSize: CGSize(width: 2048, height: 1536), viewSize: CGSize(width: 1200, height: 600))

    func testAspectFitFrameIsCentred() {
        XCTAssertEqual(geometry.scale, 600.0 / 1536.0, accuracy: 1e-9)
        XCTAssertEqual(geometry.imageFrame.width, 800, accuracy: 1e-9)
        XCTAssertEqual(geometry.imageFrame.minX, 200, accuracy: 1e-9)
        XCTAssertEqual(geometry.imageFrame.minY, 0, accuracy: 1e-9)
    }

    func testViewPointMapsToImagePoint() throws {
        let centre = try XCTUnwrap(geometry.imagePoint(fromView: CGPoint(x: 600, y: 300)))
        XCTAssertEqual(centre.x, 1024, accuracy: 1e-6)
        XCTAssertEqual(centre.y, 768, accuracy: 1e-6)
    }

    func testTouchesInTheLetterboxAreIgnored() {
        XCTAssertNil(geometry.imagePoint(fromView: CGPoint(x: 100, y: 300)))
        XCTAssertNil(geometry.imagePoint(fromView: CGPoint(x: 1100, y: 300)))
    }
}
