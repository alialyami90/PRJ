import Foundation
import Observation

/// Dependency container injected at the root. Features read services from here
/// instead of constructing them, so tests and previews can swap in fakes.
@Observable
final class AppEnvironment {
    let catalog: SceneCatalog
    let ads: AdService
    let persistence: PersistenceService
    let rewards: RewardStore
    /// Bumped after a page's progress or thumbnail is saved, so the gallery redraws.
    var libraryVersion = 0

    init(catalog: SceneCatalog, ads: AdService, persistence: PersistenceService, rewards: RewardStore) {
        self.catalog = catalog
        self.ads = ads
        self.persistence = persistence
        self.rewards = rewards
    }

    static func live() -> AppEnvironment {
        AppEnvironment(
            catalog: SceneCatalog.loadFromBundle(),
            ads: liveAds(),
            persistence: FilePersistenceService(),
            rewards: RewardStore()
        )
    }

    /// AdMob once its package is added (see docs/MONETIZATION.md); no ads until then.
    private static func liveAds() -> AdService {
        #if canImport(GoogleMobileAds)
        return AdMobAdService()
        #else
        return NoOpAdService()
        #endif
    }

    static func preview() -> AppEnvironment {
        AppEnvironment(catalog: .sample, ads: NoOpAdService(), persistence: InMemoryPersistenceService(),
                       rewards: RewardStore(defaults: UserDefaults(suiteName: "preview") ?? .standard))
    }
}
