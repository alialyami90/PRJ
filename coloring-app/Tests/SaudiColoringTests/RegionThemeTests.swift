import XCTest
@testable import SaudiColoring

final class RegionThemeTests: XCTestCase {
    /// Every shipped region wears its own ornament: nine regions, nine different motifs.
    func testEveryRegionHasItsOwnMotif() {
        let regions = SceneCatalog.loadFromBundle().regions
        let motifs = regions.map { "\(RegionTheme.of($0.id).motif)" }
        XCTAssertEqual(Set(motifs).count, regions.count, motifs.joined(separator: ", "))
    }

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
