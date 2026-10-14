import SwiftUI

/// Shown once when a page is finished.
struct CelebrationView: View {
    /// Nil once the bonus colours are unlocked.
    let onUnlockBonus: (() -> Void)?
    let onKeepColoring: () -> Void
    let onMorePictures: () -> Void
    @State private var appeared = false

    init(onUnlockBonus: (() -> Void)?, onKeepColoring: @escaping () -> Void, onMorePictures: @escaping () -> Void) {
        self.onUnlockBonus = onUnlockBonus
        self.onKeepColoring = onKeepColoring
        self.onMorePictures = onMorePictures
    }

    var body: some View {
        VStack(spacing: 24) {
            HStack(spacing: 12) {
                ForEach(0..<3) { i in
                    Image(systemName: "star.fill")
                        .font(.system(size: i == 1 ? 72 : 52))
                        .foregroundStyle(.yellow)
                        .shadow(color: .orange.opacity(0.5), radius: 6)
                        .scaleEffect(appeared ? 1 : 0.2)
                        .rotationEffect(.degrees(appeared ? 0 : -90))
                        .animation(.spring(duration: 0.6, bounce: 0.5).delay(0.15 * Double(i)), value: appeared)
                }
            }
            Text("You did it!")
                .font(.system(size: 44, weight: .heavy, design: .rounded))
            VStack(spacing: 14) {
                if let onUnlockBonus {
                    big("Get more colours", systemImage: "paintpalette.fill", tint: .orange, action: onUnlockBonus)
                }
                big("Keep coloring", systemImage: "paintbrush.fill", tint: .accentColor, action: onKeepColoring)
                big("More pictures", systemImage: "square.grid.2x2.fill", tint: .green, action: onMorePictures)
            }
        }
        .padding(40)
        .background(.regularMaterial, in: RoundedRectangle(cornerRadius: 32))
        .shadow(radius: 20)
        .padding()
        .onAppear { appeared = true }
    }

    private func big(_ title: LocalizedStringKey, systemImage: String, tint: Color, action: @escaping () -> Void) -> some View {
        Button(action: action) {
            Label(title, systemImage: systemImage)
                .font(.title2.bold())
                .frame(maxWidth: 360, minHeight: 60)
        }
        .buttonStyle(.borderedProminent)
        .tint(tint)
    }
}

#Preview {
    CelebrationView(onUnlockBonus: {}, onKeepColoring: {}, onMorePictures: {})
}
