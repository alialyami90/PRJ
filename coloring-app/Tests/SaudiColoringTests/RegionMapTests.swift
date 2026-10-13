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
}
