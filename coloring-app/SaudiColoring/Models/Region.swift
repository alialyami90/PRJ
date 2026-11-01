import Foundation

struct Region: Identifiable, Codable, Hashable {
    let id: String
    let name: String
    let nameAr: String
    let order: Int
    let scenes: [ColoringScene]
}

struct ColoringScene: Identifiable, Codable, Hashable {
    enum Difficulty: String, Codable { case easy, medium, hard }

    let id: String
    /// A short name, two to four words, in English and Arabic.
    let title: String
    let titleAr: String
    let difficulty: Difficulty

    /// The title in the app's language: Arabic when the app runs in Arabic and the scene has one.
    var displayTitle: String {
        AppLanguage.isArabic && !titleAr.isEmpty ? titleAr : title
    }
}

/// Which of the app's two languages it is running in (the first of the app's own localizations the
/// device prefers), for content that carries both names rather than going through the string catalog.
enum AppLanguage {
    static var isArabic: Bool { isArabic(Bundle.main.preferredLocalizations) }

    static func isArabic(_ preferred: [String]) -> Bool {
        preferred.first?.lowercased().hasPrefix("ar") == true
    }
}

/// Loaded from Resources/Scenes/catalog.json (written by Scripts/sync_scenes.py).
struct SceneCatalog: Codable {
    let regions: [Region]

    static func loadFromBundle() -> SceneCatalog {
        guard let url = Bundle.main.url(forResource: "catalog", withExtension: "json", subdirectory: "Scenes"),
              let data = try? Data(contentsOf: url),
              let regions = try? JSONDecoder().decode([Region].self, from: data),
              !regions.isEmpty // no scene approved yet: keep the sample so the app is still playable
        else { return .sample }
        return SceneCatalog(regions: regions.sorted { $0.order < $1.order })
    }

    static let sample = SceneCatalog(regions: [
        Region(id: "riyadh", name: "Riyadh", nameAr: "الرياض", order: 0, scenes: [
            ColoringScene(id: "masmak-fort", title: "Masmak Fort", titleAr: "قصر المصمك", difficulty: .easy)
        ])
    ])
}
