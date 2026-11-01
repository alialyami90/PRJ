import XCTest
@testable import SaudiColoring

final class AdsTests: XCTestCase {
    func testInterstitialWaitsForThreePagesAndTwoMinutes() {
        let start = Date(timeIntervalSince1970: 0)
        var policy = InterstitialPolicy(sessionStart: start)
        policy.pageFinished()
        policy.pageFinished()
        XCTAssertFalse(policy.shouldShow(at: start.addingTimeInterval(600)))
        policy.pageFinished()
        XCTAssertFalse(policy.shouldShow(at: start.addingTimeInterval(60)), "never in the first two minutes")
        XCTAssertTrue(policy.shouldShow(at: start.addingTimeInterval(121)))
        policy.didShow()
        XCTAssertFalse(policy.shouldShow(at: start.addingTimeInterval(600)))
    }

    func testParentalGateAsksAGrownUpSumAndChecksTheTypedAnswer() {
        var rng = SystemRandomNumberGenerator()
        for _ in 0..<200 {
            let q = ParentalGateQuestion.random(using: &rng)
            XCTAssertTrue((12...19).contains(q.a))
            XCTAssertTrue((3...9).contains(q.b))
            XCTAssertGreaterThanOrEqual(q.answer, 36, "too easy for a grown-up-only gate")
            XCTAssertLessThanOrEqual(String(q.answer).count, ParentalGateQuestion.maxDigits)
            XCTAssertTrue(q.isRight(String(q.answer)))
            XCTAssertFalse(q.isRight(String(q.answer + 1)))
            XCTAssertFalse(q.isRight(""))
        }
    }

    func testBonusColoursStayUnlocked() throws {
        let suite = "test-\(UUID().uuidString)"
        let defaults = try XCTUnwrap(UserDefaults(suiteName: suite))
        defer { defaults.removePersistentDomain(forName: suite) }
        XCTAssertFalse(RewardStore(defaults: defaults).bonusColorsUnlocked)
        RewardStore(defaults: defaults).unlockBonusColors()
        XCTAssertTrue(RewardStore(defaults: defaults).bonusColorsUnlocked)
    }

    func testNoAdNetworkMeansRewardsAreFree() {
        let ads = NoOpAdService()
        var rewarded = false
        ads.showRewarded { rewarded = true }
        XCTAssertTrue(rewarded)
        ads.pageFinished()
        ads.showInterstitialIfEligible()
        XCTAssertFalse(ads.isBannerAvailable)
        XCTAssertNil(ads.makeBannerView())
    }
}
