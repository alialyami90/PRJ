import Foundation
import UIKit

/// The only door to any ad SDK. Implementations must be configured child-directed
/// (see docs/MONETIZATION.md). Features never import an ad SDK.
protocol AdService: AnyObject {
    func start()
    /// Banner shown under the gallery, never over the canvas.
    var isBannerAvailable: Bool { get }
    /// A fresh banner for the gallery, or nil when there is none to show.
    func makeBannerView() -> UIView?
    /// Call each time the child finishes a page; it counts towards `InterstitialPolicy`.
    func pageFinished()
    /// Call as a new page opens (between pages, never right after a finish); the service applies
    /// `InterstitialPolicy`.
    func showInterstitialIfEligible()
    /// Whether a rewarded ad is ready. When false, rewards are simply given (see `RewardStore`).
    var isRewardedAvailable: Bool { get }
    /// Rewarded video. Caller must have passed the parental gate first.
    func showRewarded(onReward: @escaping () -> Void)
}

/// No ads at all: previews, tests, and builds without an ad network.
final class NoOpAdService: AdService {
    func start() {}
    var isBannerAvailable: Bool { false }
    func makeBannerView() -> UIView? { nil }
    func pageFinished() {}
    func showInterstitialIfEligible() {}
    var isRewardedAvailable: Bool { false }
    func showRewarded(onReward: @escaping () -> Void) { onReward() }
}

/// When an interstitial may interrupt: only as a new page opens, at most one per `pagesBetweenAds`
/// finished pages, and never in the first `minimumSessionAge` seconds of a session.
struct InterstitialPolicy {
    var sessionStart: Date
    var minimumSessionAge: TimeInterval = 120
    var pagesBetweenAds = 3
    private(set) var pagesSinceLastAd = 0

    init(sessionStart: Date = .now) {
        self.sessionStart = sessionStart
    }

    mutating func pageFinished() { pagesSinceLastAd += 1 }

    func shouldShow(at now: Date = .now) -> Bool {
        pagesSinceLastAd >= pagesBetweenAds && now.timeIntervalSince(sessionStart) >= minimumSessionAge
    }

    mutating func didShow() { pagesSinceLastAd = 0 }
}

extension UIApplication {
    /// The view controller an ad SDK should present from: the top of the key window.
    var topViewController: UIViewController? {
        let window = connectedScenes
            .compactMap { $0 as? UIWindowScene }
            .flatMap(\.windows)
            .first(where: \.isKeyWindow)
        var top = window?.rootViewController
        while let presented = top?.presentedViewController { top = presented }
        return top
    }
}
