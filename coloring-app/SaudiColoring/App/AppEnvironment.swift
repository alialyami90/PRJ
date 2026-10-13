import Foundation
import Observation

/// Dependency container injected at the root. Features read services from here
/// instead of constructing them, so tests and previews can swap in fakes.
@Observable
final class AppEnvironment {
    let catalog: SceneCatalog
    let ads: AdService
    let persistence: PersistenceService

    init(catalog: SceneCatalog, ads: AdService, persistence: PersistenceService) {
        self.catalog = catalog
        self.ads = ads
        self.persistence = persistence
    }

    static func live() -> AppEnvironment {
        AppEnvironment(
            catalog: SceneCatalog.loadFromBundle(),
            ads: NoOpAdService(), // swap for AdMobAdService once the SDK is wired (see docs/MONETIZATION.md)
            persistence: FilePersistenceService()
        )
    }

    static func preview() -> AppEnvironment {
        AppEnvironment(catalog: .sample, ads: NoOpAdService(), persistence: InMemoryPersistenceService())
    }
}
