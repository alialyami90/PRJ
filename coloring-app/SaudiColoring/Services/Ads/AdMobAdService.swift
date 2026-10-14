#if canImport(GoogleMobileAds)
import GoogleMobileAds
import UIKit

/// Google AdMob, configured for the Kids Category: child-directed, G-rated, no tracking.
/// Compiled only once the GoogleMobileAds package is added in project.yml (see docs/MONETIZATION.md).
/// Written against Google Mobile Ads SDK 11.x.
final class AdMobAdService: NSObject, AdService {
    struct UnitIDs {
        var banner: String
        var interstitial: String
        var rewarded: String

        /// Google's public test units: they always fill and never pay. Replace with the app's own
        /// units from the AdMob console before release, and set GADApplicationIdentifier in project.yml.
        static let test = UnitIDs(
            banner: "ca-app-pub-3940256099942544/2934735716",
            interstitial: "ca-app-pub-3940256099942544/4411468910",
            rewarded: "ca-app-pub-3940256099942544/1712485313"
        )
    }

    private let units: UnitIDs
    private var policy = InterstitialPolicy()
    private var interstitial: GADInterstitialAd?
    private var rewarded: GADRewardedAd?
    private var started = false

    init(units: UnitIDs = .test) {
        self.units = units
    }

    func start() {
        guard !started else { return }
        started = true
        let config = GADMobileAds.sharedInstance().requestConfiguration
        config.tagForChildDirectedTreatment = true
        config.tagForUnderAgeOfConsent = true
        config.maxAdContentRating = .general
        GADMobileAds.sharedInstance().start { [weak self] _ in
            self?.loadInterstitial()
            self?.loadRewarded()
        }
    }

    var isBannerAvailable: Bool { started }

    func makeBannerView() -> UIView? {
        guard started else { return nil }
        let banner = GADBannerView(adSize: GADAdSizeBanner)
        banner.adUnitID = units.banner
        banner.rootViewController = UIApplication.shared.topViewController
        banner.load(GADRequest())
        return banner
    }

    func showInterstitialIfEligible() {
        policy.pageFinished()
        guard policy.shouldShow(), let ad = interstitial, let root = UIApplication.shared.topViewController else { return }
        policy.didShow()
        interstitial = nil
        ad.present(fromRootViewController: root)
        loadInterstitial()
    }

    var isRewardedAvailable: Bool { rewarded != nil }

    func showRewarded(onReward: @escaping () -> Void) {
        guard let ad = rewarded, let root = UIApplication.shared.topViewController else { return }
        rewarded = nil
        ad.present(fromRootViewController: root) { onReward() }
        loadRewarded()
    }

    private func loadInterstitial() {
        GADInterstitialAd.load(withAdUnitID: units.interstitial, request: GADRequest()) { [weak self] ad, _ in
            self?.interstitial = ad
        }
    }

    private func loadRewarded() {
        GADRewardedAd.load(withAdUnitID: units.rewarded, request: GADRequest()) { [weak self] ad, _ in
            self?.rewarded = ad
        }
    }
}
#endif
