import Foundation

/// Colours are stored as "#RRGGBB" strings in documents and palettes; the engine works in packed 0xRRGGBB.
enum SceneColor {
    /// Parses "#RRGGBB" (the leading # is optional). Returns nil for anything else.
    static func rgb(fromHex hex: String) -> UInt32? {
        let digits = hex.hasPrefix("#") ? hex.dropFirst() : Substring(hex)
        guard digits.count == 6, digits.allSatisfy(\.isHexDigit) else { return nil }
        return UInt32(digits, radix: 16)
    }

    static func hex(_ rgb: UInt32) -> String {
        String(format: "#%06X", rgb & 0xFFFFFF)
    }
}
