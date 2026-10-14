import Foundation

protocol PersistenceService {
    func load(regionId: String, sceneId: String) -> ColoringDocument?
    func save(_ document: ColoringDocument) throws
    func delete(regionId: String, sceneId: String)
}

/// JSON files in Application Support/Documents/<region>/<scene>.json
final class FilePersistenceService: PersistenceService {
    private let root: URL
    private let encoder = JSONEncoder()
    private let decoder = JSONDecoder()

    init(root: URL = FileManager.default.urls(for: .applicationSupportDirectory, in: .userDomainMask)[0]
            .appendingPathComponent("Documents", isDirectory: true)) {
        self.root = root
    }

    private func url(_ regionId: String, _ sceneId: String) -> URL {
        root.appendingPathComponent(regionId, isDirectory: true).appendingPathComponent("\(sceneId).json")
    }

    func load(regionId: String, sceneId: String) -> ColoringDocument? {
        guard let data = try? Data(contentsOf: url(regionId, sceneId)) else { return nil }
        return try? decoder.decode(ColoringDocument.self, from: data)
    }

    func save(_ document: ColoringDocument) throws {
        let target = url(document.regionId, document.sceneId)
        try FileManager.default.createDirectory(at: target.deletingLastPathComponent(), withIntermediateDirectories: true)
        try encoder.encode(document).write(to: target, options: .atomic)
    }

    func delete(regionId: String, sceneId: String) {
        try? FileManager.default.removeItem(at: url(regionId, sceneId))
    }
}

final class InMemoryPersistenceService: PersistenceService {
    private var store: [String: ColoringDocument] = [:]
    func load(regionId: String, sceneId: String) -> ColoringDocument? { store["\(regionId)/\(sceneId)"] }
    func save(_ document: ColoringDocument) throws { store["\(document.regionId)/\(document.sceneId)"] = document }
    func delete(regionId: String, sceneId: String) { store["\(regionId)/\(sceneId)"] = nil }
}
