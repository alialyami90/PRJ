import XCTest
@testable import SaudiColoring

final class AppThemeTests: XCTestCase {
    func testEveryRegionHasAnArabicName() {
        for region in SceneCatalog.loadFromBundle().regions {
            XCTAssertFalse(region.nameAr.isEmpty, region.id)
        }
    }

    func testNameSplitsIntoShortNameAndArea() {
        let riyadh = Region(id: "riyadh", name: "Riyadh (Najd)", nameAr: "", order: 0, scenes: [])
        XCTAssertEqual(riyadh.shortName, "Riyadh")
        XCTAssertEqual(riyadh.area, "Najd")

        let najran = Region(id: "najran", name: "Najran", nameAr: "", order: 8, scenes: [])
        XCTAssertEqual(najran.shortName, "Najran")
        XCTAssertNil(najran.area)
    }
}
