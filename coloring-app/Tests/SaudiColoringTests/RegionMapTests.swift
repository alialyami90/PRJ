import XCTest
@testable import SaudiColoring

final class RegionMapTests: XCTestCase {
    // 3x2 map: two regions (red, blue) separated by an outline column.
    private let map = RegionMap(width: 3, height: 2, pixels: [
        0xFF0000, 0x000000, 0x0000FF,
        0xFF0000, 0x000000, 0x0000FF,
    ])

    func testRegionLookup() {
        XCTAssertEqual(map.regionId(at: CGPoint(x: 0, y: 1)), 0xFF0000)
        XCTAssertEqual(map.regionId(at: CGPoint(x: 2, y: 0)), 0x0000FF)
    }

    func testOutlineAndOutOfBoundsReturnNil() {
        XCTAssertNil(map.regionId(at: CGPoint(x: 1, y: 0)))
        XCTAssertNil(map.regionId(at: CGPoint(x: -1, y: 0)))
        XCTAssertNil(map.regionId(at: CGPoint(x: 3, y: 0)))
    }

    func testRegionIdsExcludeOutline() {
        XCTAssertEqual(map.regionIds, [0xFF0000, 0x0000FF])
    }

    func testPaperIsNotARegion() {
        // red | paper | blue: paper cannot be tapped or filled, and a tap on it finds the nearest region.
        let map = RegionMap(width: 3, height: 1, pixels: [0xFF0000, RegionMap.paper, 0x0000FF])
        XCTAssertNil(map.regionId(at: CGPoint(x: 1, y: 0)))
        XCTAssertNotNil(map.regionId(near: CGPoint(x: 1, y: 0), radius: 1))
        XCTAssertEqual(map.regionIds, [0xFF0000, 0x0000FF])
    }
}
