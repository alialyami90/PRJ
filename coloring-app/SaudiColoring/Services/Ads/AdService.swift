import Foundation

/// The only door to any ad SDK. Implementations must be configured child-directed
/// (see docs/MONETIZATION.md). Features never import an ad SDK.
protocol AdService: AnyObject {
    func start()
    /// Banner shown under the gallery, never over the canvas.
    var isBannerAvailable: Bool { get }
    /// Call after a scene is completed; the service applies its own frequency cap.
    func showInterstitialIfEligible()
    /// Rewarded video. Caller must have passed the parental gate first.
    func showRewarded(onReward: @escaping () -> Void)
}

final class NoOpAdService: AdService {
    func start() {}
    var isBannerAvailable: Bool { false }
    func showInterstitialIfEligible() {}
    func showRewarded(onReward: @escaping () -> Void) {}
}
