import XCTest
@testable import SaudiColoring

final class CatalogTests: XCTestCase {
    /// Scenes/catalog.json is written by Scripts/sync_scenes.py; all nine regions ship with real pages.
    func testBundleShipsNineRegionsOfEightPages() {
        let catalog = SceneCatalog.loadFromBundle()
        XCTAssertEqual(catalog.regions.count, 9)
        XCTAssertTrue(catalog.regions.allSatisfy { $0.scenes.count == 8 })
        XCTAssertEqual(catalog.regions.map(\.order), Array(0..<9))
        XCTAssertEqual(catalog.regions.last?.id, "najran")
    }

    func testEveryPageHasItsArtThumbnailAndCover() {
        for region in SceneCatalog.loadFromBundle().regions {
            XCTAssertNotNil(BundleImages.cover(regionId: region.id), region.id)
            for scene in region.scenes {
                let dir = "Scenes/\(region.id)/\(scene.id)"
                XCTAssertNotNil(BundleImages.thumbnail(regionId: region.id, sceneId: scene.id), dir)
                XCTAssertNotNil(Bundle.main.url(forResource: "regions", withExtension: "png", subdirectory: dir), dir)
                XCTAssertNotNil(Bundle.main.url(forResource: "palette", withExtension: "json", subdirectory: dir), dir)
            }
        }
    }
}
