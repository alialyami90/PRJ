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

    /// palette.json on disk is a bare array of entries.
    static func decode(from data: Data) throws -> Palette {
        Palette(entries: try JSONDecoder().decode([PaletteEntry].self, from: data))
    }

    func entry(for regionId: UInt32) -> PaletteEntry? {
        entries.first { $0.regionId == regionId }
    }

    /// Distinct colours in number order, used as the colour tray in PBN mode
    /// and as the "suggested" row in Fill mode.
    var swatches: [Swatch] {
        var seen = Set<Int>()
        var result: [Swatch] = []
        for entry in entries where seen.insert(entry.number).inserted {
            result.append(Swatch(number: entry.number, color: entry.color))
        }
        return result.sorted { $0.number < $1.number }
    }

    struct Swatch: Hashable {
        let number: Int
        let color: String
    }
}
