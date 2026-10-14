import XCTest
@testable import SaudiColoring

final class RegionLabelsTests: XCTestCase {
    func testLabelSitsInTheMiddleOfASquare() throws {
        let map = RegionMap(width: 5, height: 5, pixels: [UInt32](repeating: 0x123456, count: 25))
        let label = try XCTUnwrap(map.labels()[0x123456])
        XCTAssertEqual(label.point, CGPoint(x: 2.5, y: 2.5))
        XCTAssertEqual(label.radius, 3)
    }

    func testLabelOfAnLShapeIsInsideIt() throws {
        // 9x9: an L (three columns down the left, three rows along the bottom) around a square.
        let l: UInt32 = 0xFF0000, square: UInt32 = 0x0000FF
        var pixels = [UInt32](repeating: square, count: 81)
        for y in 0..<9 { for x in 0..<9 where x < 3 || y >= 6 { pixels[y * 9 + x] = l } }
        let map = RegionMap(width: 9, height: 9, pixels: pixels)
        let labels = map.labels()
        XCTAssertEqual(Set(labels.keys), [l, square])
        XCTAssertEqual(map.regionId(at: try XCTUnwrap(labels[l]).point), l)
        XCTAssertEqual(map.regionId(at: try XCTUnwrap(labels[square]).point), square)
    }

    func testOutlineHasNoLabel() {
        let map = RegionMap(width: 3, height: 1, pixels: [0xFF0000, 0x000000, 0x0000FF])
        XCTAssertEqual(Set(map.labels().keys), [0xFF0000, 0x0000FF])
    }

    func testEveryRealPageLabelLandsInItsOwnRegion() throws {
        let assets = try SceneAssets.load(regionId: "najran", sceneId: "al-aan-palace")
        XCTAssertFalse(assets.isSample, "Najran pages should be in the bundle")
        let labels = assets.map.labels()
        XCTAssertEqual(Set(labels.keys), assets.map.regionIds)
        for (id, label) in labels {
            XCTAssertEqual(assets.map.regionId(at: label.point), id)
        }
    }
}
