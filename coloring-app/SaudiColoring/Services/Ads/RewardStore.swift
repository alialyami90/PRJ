import Foundation
import Observation

/// What the child has unlocked with a rewarded ad. Kept on the device only.
@Observable
final class RewardStore {
    private static let bonusColorsKey = "rewards.bonusColorsUnlocked"
    private let defaults: UserDefaults
    private(set) var bonusColorsUnlocked: Bool

    init(defaults: UserDefaults = .standard) {
        self.defaults = defaults
        bonusColorsUnlocked = defaults.bool(forKey: Self.bonusColorsKey)
    }

    func unlockBonusColors() {
        bonusColorsUnlocked = true
        defaults.set(true, forKey: Self.bonusColorsKey)
    }
}
