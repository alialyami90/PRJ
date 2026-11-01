import Foundation

/// A plain name for a paint colour, so VoiceOver can say "light blue" instead of a hex code.
/// Approximate on purpose: a child needs to tell the crayons apart, not match a paint chart.
struct ColorName: Equatable {
    enum Hue: Equatable { case red, orange, yellow, green, teal, blue, purple, pink, brown, gray, black, white }
    enum Shade: Equatable { case light, plain, dark }

    let hue: Hue
    let shade: Shade

    init(hue: Hue, shade: Shade = .plain) {
        self.hue = hue
        self.shade = shade
    }

    init(hex: String) {
        let rgb = SceneColor.rgb(fromHex: hex) ?? 0xFFFFFF
        let r = Double(rgb >> 16 & 0xFF) / 255, g = Double(rgb >> 8 & 0xFF) / 255, b = Double(rgb & 0xFF) / 255
        let high = max(r, g, b), low = min(r, g, b)
        let delta = high - low
        let lightness = (high + low) / 2
        let saturation = delta == 0 ? 0 : delta / (1 - abs(2 * lightness - 1))

        let shade: Shade = lightness > 0.72 ? .light : (lightness < 0.3 ? .dark : .plain)
        // Greys, black and white.
        if saturation < 0.2 || delta < 0.08 {
            if lightness > 0.9 { self.init(hue: .white) } else if lightness < 0.15 { self.init(hue: .black) } else {
                self.init(hue: .gray, shade: shade)
            }
            return
        }

        var degrees: Double
        if high == r {
            degrees = 60 * ((g - b) / delta).truncatingRemainder(dividingBy: 6)
        } else if high == g {
            degrees = 60 * ((b - r) / delta + 2)
        } else {
            degrees = 60 * ((r - g) / delta + 4)
        }
        if degrees < 0 { degrees += 360 }

        switch degrees {
        case 15..<45:
            // Dark or dull orange reads as brown (wood, earth, tan).
            if lightness < 0.45 || saturation < 0.5 {
                self.init(hue: .brown, shade: lightness > 0.72 ? .light : .plain)
            } else {
                self.init(hue: .orange, shade: shade)
            }
        case 45..<70:
            self.init(hue: lightness < 0.3 ? .brown : .yellow, shade: lightness < 0.3 ? .plain : shade)
        case 70..<165: self.init(hue: .green, shade: shade)
        case 165..<195: self.init(hue: .teal, shade: shade)
        case 195..<255: self.init(hue: .blue, shade: shade)
        case 255..<300: self.init(hue: .purple, shade: shade)
        case 300..<345: self.init(hue: .pink, shade: shade)
        default: self.init(hue: .red, shade: shade)
        }
    }
}
