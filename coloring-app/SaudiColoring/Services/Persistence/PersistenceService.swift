import Foundation

protocol PersistenceService {
    func load(regionId: String, sceneId: String) -> ColoringDocument?
    func save(_ document: ColoringDocument) throws
    func delete(regionId: String, sceneId: String)
    /// PNG of the page as the child left it, for the gallery.
    func thumbnail(regionId: String, sceneId: String) -> Data?
    func saveThumbnail(_ png: Data, regionId: String, sceneId: String) throws
}

/// JSON files in Application Support/Documents/<region>/<scene>.json, thumbnails next to them as <scene>.png.
final class FilePersistenceService: PersistenceService {
    private let root: URL
    private let encoder = JSONEncoder()
    private let decoder = JSONDecoder()

    init(root: URL = FileManager.default.urls(for: .applicationSupportDirectory, in: .userDomainMask)[0]
            .appendingPathComponent("Documents", isDirectory: true)) {
        self.root = root
    }

    private func url(_ regionId: String, _ sceneId: String, _ ext: String = "json") -> URL {
        root.appendingPathComponent(regionId, isDirectory: true).appendingPathComponent("\(sceneId).\(ext)")
    }

    func load(regionId: String, sceneId: String) -> ColoringDocument? {
        guard let data = try? Data(contentsOf: url(regionId, sceneId)) else { return nil }
        return try? decoder.decode(ColoringDocument.self, from: data)
    }

    func save(_ document: ColoringDocument) throws {
        try write(encoder.encode(document), to: url(document.regionId, document.sceneId))
    }

    func delete(regionId: String, sceneId: String) {
        try? FileManager.default.removeItem(at: url(regionId, sceneId))
        try? FileManager.default.removeItem(at: url(regionId, sceneId, "png"))
    }

    func thumbnail(regionId: String, sceneId: String) -> Data? {
        try? Data(contentsOf: url(regionId, sceneId, "png"))
    }

    func saveThumbnail(_ png: Data, regionId: String, sceneId: String) throws {
        try write(png, to: url(regionId, sceneId, "png"))
    }

    private func write(_ data: Data, to target: URL) throws {
        try FileManager.default.createDirectory(at: target.deletingLastPathComponent(), withIntermediateDirectories: true)
        try data.write(to: target, options: .atomic)
    }
}

final class InMemoryPersistenceService: PersistenceService {
    private var store: [String: ColoringDocument] = [:]
    private var thumbnails: [String: Data] = [:]
    func load(regionId: String, sceneId: String) -> ColoringDocument? { store["\(regionId)/\(sceneId)"] }
    func save(_ document: ColoringDocument) throws { store["\(document.regionId)/\(document.sceneId)"] = document }
    func delete(regionId: String, sceneId: String) {
        store["\(regionId)/\(sceneId)"] = nil
        thumbnails["\(regionId)/\(sceneId)"] = nil
    }
    func thumbnail(regionId: String, sceneId: String) -> Data? { thumbnails["\(regionId)/\(sceneId)"] }
    func saveThumbnail(_ png: Data, regionId: String, sceneId: String) throws { thumbnails["\(regionId)/\(sceneId)"] = png }
}
