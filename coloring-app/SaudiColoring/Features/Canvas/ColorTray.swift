import SwiftUI

/// Big round swatches a small finger can hit: the scene's suggested colours first, then a fixed crayon box,
/// then the bonus colours (or, while they are locked, a button to unlock them).
struct ColorTray: View {
    let suggested: [String]
    @Binding var selection: String
    var bonus: [String] = []
    /// Shown instead of the bonus colours while they are locked.
    var onUnlockBonus: (() -> Void)?

    static let crayons = [
        "#E53935", "#FB8C00", "#FDD835", "#43A047", "#00897B", "#1E88E5",
        "#3949AB", "#8E24AA", "#D81B60", "#6D4C41", "#9E9E9E", "#212121", "#FFFFFF",
    ]

    /// Unlocked by a rewarded ad after finishing a page (see RewardStore).
    static let bonusColors = [
        "#FF8A80", "#FFD180", "#FFFF8D", "#B9F6CA", "#84FFFF", "#82B1FF", "#B388FF", "#FF80AB",
        "#C0A062", "#B0BEC5",
    ]

    var body: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 12) {
                ForEach(suggested, id: \.self) { swatch($0) }
                if !suggested.isEmpty {
                    Divider().frame(height: 48)
                }
                ForEach(Self.crayons.filter { !suggested.contains($0) }, id: \.self) { swatch($0) }
                if !bonus.isEmpty || onUnlockBonus != nil {
                    Divider().frame(height: 48)
                }
                ForEach(bonus.filter { !suggested.contains($0) }, id: \.self) { swatch($0) }
                if let onUnlockBonus {
                    Button(action: onUnlockBonus) {
                        Label("More colours", systemImage: "lock.fill")
                            .font(.headline)
                            .fontDesign(.rounded)
                            .frame(minWidth: 60, minHeight: 60)
                            .padding(.horizontal, 16)
                            .background(Color.primary.opacity(0.08), in: Capsule())
                            .overlay(Capsule().strokeBorder(Color.primary.opacity(0.2), lineWidth: 1.5))
                    }
                    .buttonStyle(.plain)
                }
            }
            .padding(.horizontal)
            .padding(.vertical, 8)
        }
    }

    private func swatch(_ hex: String) -> some View {
        let isSelected = hex == selection
        return Button {
            selection = hex
        } label: {
            Circle()
                .fill(Color(hex: hex))
                .overlay(Circle().strokeBorder(.black.opacity(0.25), lineWidth: 2))
                .overlay(Circle().strokeBorder(.primary, lineWidth: isSelected ? 5 : 0).padding(-8))
                .frame(width: 60, height: 60)
                .scaleEffect(isSelected ? 1.1 : 1)
                .animation(.spring(duration: 0.2), value: isSelected)
                .padding(8)
        }
        .buttonStyle(.plain)
        .accessibilityLabel(Text("Colour \(hex)"))
        .accessibilityAddTraits(isSelected ? .isSelected : [])
    }
}

extension Color {
    /// "#RRGGBB" → Color; unparseable strings render as white paper.
    init(hex: String) {
        let rgb = SceneColor.rgb(fromHex: hex) ?? 0xFFFFFF
        self.init(.sRGB,
                  red: Double(rgb >> 16 & 0xFF) / 255,
                  green: Double(rgb >> 8 & 0xFF) / 255,
                  blue: Double(rgb & 0xFF) / 255)
    }
}

#Preview {
    ColorTray(suggested: ["#7EC8E3", "#FFC93C"], selection: .constant("#FFC93C"))
}
