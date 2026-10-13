import Foundation

/// One entry of a scene's palette.json: the paint-by-number answer key.
struct PaletteEntry: Codable, Hashable {
    /// RGB of this region in regions.png, packed as 0xRRGGBB.
    let regionId: UInt32
    /// The number shown to the child in Paint by Number mode.
    let number: Int
    /// Suggested colour as "#RRGGBB".
    let color: String
}

struct Palette: Codable {
    let entries: [PaletteEntry]

    func entry(for regionId: UInt32) -> PaletteEntry? {
        entries.first { $0.regionId == regionId }
    }

    /// Distinct colours in number order, used as the colour tray in PBN mode.
    var swatches: [(number: Int, color: String)] {
        var seen = Set<Int>()
        return entries.compactMap { seen.insert($0.number).inserted ? ($0.number, $0.color) : nil }
            .sorted { $0.number < $1.number }
    }
}
