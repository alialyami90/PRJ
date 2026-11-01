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

        let ahsa = Region(id: "al-ahsa", name: "Al-Ahsa (Eastern Province)", nameAr: "الأحساء (المنطقة الشرقية)", order: 2, scenes: [])
        XCTAssertEqual(ahsa.shortNameAr, "الأحساء")

        let najran = Region(id: "najran", name: "Najran", nameAr: "", order: 8, scenes: [])
        XCTAssertEqual(najran.shortName, "Najran")
        XCTAssertNil(najran.area)
    }

    func testNamesFollowTheAppLanguage() {
        let riyadh = Region(id: "riyadh", name: "Riyadh (Najd)", nameAr: "الرياض (نجد)", order: 0, scenes: [])
        XCTAssertEqual(riyadh.displayName(arabic: false), "Riyadh")
        XCTAssertEqual(riyadh.displayArea(arabic: false), "Najd")
        XCTAssertEqual(riyadh.otherName(arabic: false), "الرياض")
        XCTAssertEqual(riyadh.displayName(arabic: true), "الرياض")
        XCTAssertEqual(riyadh.displayArea(arabic: true), "نجد")
        XCTAssertEqual(riyadh.otherName(arabic: true), "Riyadh")

        let noArabic = Region(id: "x", name: "Somewhere", nameAr: "", order: 0, scenes: [])
        XCTAssertEqual(noArabic.displayName(arabic: true), "Somewhere")
        XCTAssertNil(noArabic.otherName(arabic: true))
        XCTAssertNil(noArabic.otherName(arabic: false))
    }

    func testAppLanguageIsTheFirstPreferredLocalization() {
        XCTAssertTrue(AppLanguage.isArabic(["ar"]))
        XCTAssertTrue(AppLanguage.isArabic(["ar-SA", "en"]))
        XCTAssertFalse(AppLanguage.isArabic(["en", "ar"]))
        XCTAssertFalse(AppLanguage.isArabic([]))
    }

    /// Every page has a short title in both languages: two to four words, so it fits a card on one or two lines.
    func testEverySceneHasShortTitlesInBothLanguages() {
        for region in SceneCatalog.loadFromBundle().regions {
            for scene in region.scenes {
                XCTAssertFalse(scene.titleAr.isEmpty, scene.id)
                XCTAssertLessThanOrEqual(scene.title.split(separator: " ").count, 4, scene.title)
                XCTAssertLessThanOrEqual(scene.titleAr.split(separator: " ").count, 5, scene.titleAr)
            }
        }
    }
}
