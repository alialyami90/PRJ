import XCTest
@testable import SaudiColoring

final class SceneAssetsTests: XCTestCase {
    func testScenesWithoutArtFallBackToTheSample() throws {
        let assets = try SceneAssets.load(regionId: "riyadh", sceneId: "no-such-scene")
        XCTAssertTrue(assets.isSample)
        XCTAssertEqual(assets.map.width, 2048)
        XCTAssertEqual(assets.map.height, 1536)
    }

    /// Guards the asset contract: if decoding shifted colours (colour management, interpolation),
    /// region ids would no longer match the palette and nothing could be filled.
    func testSampleMapAndPaletteAgree() throws {
        let assets = try SceneAssets.load(regionId: "riyadh", sceneId: "masmak-fort")
        let paletteIds = Set(assets.palette.entries.map(\.regionId))
        XCTAssertEqual(assets.map.regionIds, paletteIds)
        XCTAssertGreaterThanOrEqual(paletteIds.count, 10)
    }

    func testPaletteDecodesTheOnDiskArrayFormat() throws {
        let json = ##"[{"regionId": 16711680, "number": 2, "color": "#FF0000"}, {"regionId": 255, "number": 1, "color": "#0000FF"}, {"regionId": 65280, "number": 2, "color": "#FF0000"}]"##
        let palette = try Palette.decode(from: Data(json.utf8))
        XCTAssertEqual(palette.entry(for: 0xFF0000)?.number, 2)
        XCTAssertEqual(palette.swatches, [.init(number: 1, color: "#0000FF"), .init(number: 2, color: "#FF0000")])
    }
}
