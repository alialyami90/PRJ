import SwiftUI
import UIKit

/// Each region's own look: its colours and the ornament band from its own building or craft tradition.
/// The app shell (the green route rail) is shared; everything inside a region wears its theme.
struct RegionTheme {
    /// Header bands, the selected mode, stamps. White text sits on it.
    let ground: Color
    /// The page area and gallery behind the cards.
    let tint: Color
    /// Second colour of the ornament and of small highlights.
    let accent: Color
    /// Text and lines on `tint`.
    let ink: Color
    let motif: Motif

    /// The ornament band each region carries along the edge of its header and its colour tray.
    enum Motif {
        /// Riyadh: the stepped triangle crenellations (shurfat) and triangle vents of Najdi mud walls.
        case najdi
        /// Jeddah: the wooden lattice of the rawashin bay windows in Al-Balad.
        case rawashin
        /// Al-Ahsa: the plaited palm-leaf strips (khoos) of oasis baskets and mats.
        case khoos
        /// Asir: Al-Qatt Al-Asiri, the bands of stripes and triangles painted on house walls.
        case qatt
        /// AlUla: the crow-step crowns carved above the Nabataean tombs of Hegra.
        case nabataean
        /// Tabuk: the sandstone arches of Hisma and the arcades of Tabuk castle.
        case arches
        /// Jazan and Farasan: the Red Sea's waves and fish-scale coral stone.
        case waves
        /// Hail: Al-Sadu weaving of the northern Bedouin.
        case sadu
        /// Najran: the diamond weave of Najrani palm baskets.
        case diamonds
    }

    /// Text and icons on `accent`: white on the darker accents, near-black on the bright ones.
    var onAccent: Color {
        switch motif {
        case .najdi, .nabataean, .diamonds: .white
        default: Color(hex: "#1E1513")
        }
    }

    static func of(_ regionId: String) -> RegionTheme {
        themes[regionId] ?? fallback
    }

    private static let themes: [String: RegionTheme] = [
        "riyadh": RegionTheme(ground: .hex(0xA64A26, dark: 0xB4572F), tint: .hex(0xF7E8DC, dark: 0x2A1A12),
                              accent: .hex(0x2E7D78, dark: 0x4FA39C), ink: .hex(0x3B1E12, dark: 0xF7E8DC), motif: .najdi),
        "jeddah": RegionTheme(ground: .hex(0x17655F, dark: 0x1E7A73), tint: .hex(0xE3F1EE, dark: 0x0F2624),
                              accent: .hex(0xD9824C, dark: 0xE39663), ink: .hex(0x0E2F2C, dark: 0xE3F1EE), motif: .rawashin),
        "al-ahsa": RegionTheme(ground: .hex(0x45702A, dark: 0x55843A), tint: .hex(0xEEF3E1, dark: 0x1B2513),
                               accent: .hex(0xE0A83A, dark: 0xE8B656), ink: .hex(0x23331A, dark: 0xEEF3E1), motif: .khoos),
        "asir": RegionTheme(ground: .hex(0xB8312A, dark: 0xC63C33), tint: .hex(0xFCEDE9, dark: 0x2B1311),
                            accent: .hex(0xF2C230, dark: 0xF2C230), ink: .hex(0x2A1110, dark: 0xFCEDE9), motif: .qatt),
        "alula": RegionTheme(ground: .hex(0xA4552A, dark: 0xB26236), tint: .hex(0xF8E9DE, dark: 0x2A1810),
                             accent: .hex(0x5C3C7A, dark: 0x9A78BC), ink: .hex(0x3A2014, dark: 0xF8E9DE), motif: .nabataean),
        "tabuk": RegionTheme(ground: .hex(0x28527E, dark: 0x2F6194), tint: .hex(0xE7EEF6, dark: 0x111D2B),
                             accent: .hex(0xE7956A, dark: 0xEDA680), ink: .hex(0x102338, dark: 0xE7EEF6), motif: .arches),
        "jazan": RegionTheme(ground: .hex(0x0B7373, dark: 0x0F8585), tint: .hex(0xDFF3F1, dark: 0x0C2424),
                             accent: .hex(0xF2A531, dark: 0xF2A531), ink: .hex(0x083838, dark: 0xDFF3F1), motif: .waves),
        "hail": RegionTheme(ground: .hex(0x962922, dark: 0xA8342C), tint: .hex(0xF7E7E3, dark: 0x2A1311),
                            accent: .hex(0xE2A93B, dark: 0xE8B654), ink: .hex(0x1E1513, dark: 0xF7E7E3), motif: .sadu),
        "najran": RegionTheme(ground: .hex(0x7D4A2C, dark: 0x8F5735), tint: .hex(0xF5EAE2, dark: 0x271910),
                              accent: .hex(0xC2457F, dark: 0xD8679A), ink: .hex(0x2E1A10, dark: 0xF5EAE2), motif: .diamonds),
    ]

    private static let fallback = themes["riyadh"]!
}

/// The shared shell: the journey rail that holds every region.
enum Shell {
    /// Deep palm green rail behind the route.
    static let rail = Color.hex(0x0F4A38, dark: 0x0A2C22)
    /// A slightly lighter green for the selected stop's row.
    static let railSelected = Color.hex(0x1C6650, dark: 0x174535)
    /// The dashed caravan route, date gold.
    static let route = Color.hex(0xE8B04B, dark: 0xE8B04B)
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

    var theme: RegionTheme { RegionTheme.of(id) }
}

extension AppEnvironment {
    /// How many of a region's pages the child has finished. Reads `libraryVersion` so views redraw after a save.
    func finishedCount(in region: Region) -> Int {
        _ = libraryVersion
        return region.scenes.filter { persistence.load(regionId: region.id, sceneId: $0.id)?.completedAt != nil }.count
    }
}
