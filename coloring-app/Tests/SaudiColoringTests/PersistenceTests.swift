import XCTest
@testable import SaudiColoring

final class PersistenceTests: XCTestCase {
    func testDocumentRoundTripsThroughDisk() throws {
        let root = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString, isDirectory: true)
        defer { try? FileManager.default.removeItem(at: root) }
        let service = FilePersistenceService(root: root)

        var doc = ColoringDocument(regionId: "riyadh", sceneId: "masmak-fort", mode: .fill)
        doc.fills = [0xFF0000: "#123456", 0x0000FF: "#ABCDEF"]
        doc.strokes = [Stroke(color: "#000000", width: 4, points: [.init(x: 1, y: 2), .init(x: 3, y: 4)])]
        try service.save(doc)

        let loaded = try XCTUnwrap(service.load(regionId: "riyadh", sceneId: "masmak-fort"))
        XCTAssertEqual(loaded.fills, doc.fills)
        XCTAssertEqual(loaded.strokes, doc.strokes)

        service.delete(regionId: "riyadh", sceneId: "masmak-fort")
        XCTAssertNil(service.load(regionId: "riyadh", sceneId: "masmak-fort"))
    }
}

final class SceneColorTests: XCTestCase {
    func testHexRoundTrip() {
        XCTAssertEqual(SceneColor.rgb(fromHex: "#F4A62A"), 0xF4A62A)
        XCTAssertEqual(SceneColor.rgb(fromHex: "f4a62a"), 0xF4A62A)
        XCTAssertEqual(SceneColor.hex(0xF4A62A), "#F4A62A")
        XCTAssertNil(SceneColor.rgb(fromHex: "#F4A6"))
        XCTAssertNil(SceneColor.rgb(fromHex: "#GGGGGG"))
    }
}
