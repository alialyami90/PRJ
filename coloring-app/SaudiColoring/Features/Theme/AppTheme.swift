import SwiftUI
import UIKit

/// One Saudi look for the whole app: palm green, date gold, a sage-white ground, and the Sadu band
/// (see `SaduBand`) along the edges of headers and trays. Every region shares it; the pages carry the variety.
struct AppTheme {
    /// Header bands, the selected mode, stamps. White text sits on it.
    let ground: Color
    /// The page area and gallery behind the cards.
    let tint: Color
    /// Date gold: stops on the route, stamp rings, the "more colours" button.
    let accent: Color
    /// Text and lines on `tint`.
    let ink: Color
    /// Text and icons on `accent`.
    let onAccent: Color

    static let saudi = AppTheme(
        ground: .hex(0x11563F, dark: 0x17694D),
        tint: .hex(0xEDF2EC, dark: 0x0F1A15),
        accent: .hex(0xE2A63B, dark: 0xE8B04B),
        ink: .hex(0x13261E, dark: 0xEDF2EC),
        onAccent: .hex(0x1E1513, dark: 0x1E1513)
    )
}

/// The journey rail that holds every region.
enum Shell {
    /// Deep palm green rail behind the route, a step darker than the headers.
    static let rail = Color.hex(0x0B3A2C, dark: 0x082619)
    /// A lighter green for the selected stop's row.
    static let railSelected = Color.hex(0x17604A, dark: 0x134433)
    /// The dotted caravan route, date gold.
    static let route = Color.hex(0xE2A63B, dark: 0xE8B04B)
    /// Text on the rail.
    static let railText = Color.white
    static let railSecondary = Color.white.opacity(0.72)
}

extension Color {
    /// A colour with its own dark-mode value, from 0xRRGGBB.
    static func hex(_ light: UInt32, dark: UInt32) -> Color {
        Color(UIColor { traits in
            UIColor(rgb: traits.userInterfaceStyle == .dark ? dark : light)
        })
    }
}

private extension UIColor {
    convenience init(rgb: UInt32) {
        self.init(red: CGFloat(rgb >> 16 & 0xFF) / 255, green: CGFloat(rgb >> 8 & 0xFF) / 255,
                  blue: CGFloat(rgb & 0xFF) / 255, alpha: 1)
    }
}

extension Region {
    /// "Riyadh (Najd)" → "Riyadh"; the part in brackets is `area`.
    var shortName: String {
        guard let open = name.range(of: " (") else { return name }
        return String(name[..<open.lowerBound])
    }

    /// "Riyadh (Najd)" → "Najd"; nil when the name has no brackets.
    var area: String? {
        guard let open = name.range(of: " ("), name.hasSuffix(")") else { return nil }
        return String(name[open.upperBound..<name.index(before: name.endIndex)])
    }
}

extension AppEnvironment {
    /// How many of a region's pages the child has finished. Reads `libraryVersion` so views redraw after a save.
    func finishedCount(in region: Region) -> Int {
        _ = libraryVersion
        return region.scenes.filter { persistence.load(regionId: region.id, sceneId: $0.id)?.completedAt != nil }.count
    }
}
