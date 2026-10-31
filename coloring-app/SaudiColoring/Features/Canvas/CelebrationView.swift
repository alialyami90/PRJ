import SwiftUI

/// Shown once when a page is finished: the stamp presses down onto the card, then three big choices.
struct CelebrationView: View {
    let theme: AppTheme
    /// Nil once the bonus colours are unlocked.
    let onUnlockBonus: (() -> Void)?
    let onKeepColoring: () -> Void
    let onMorePictures: () -> Void
    @State private var stamped = false
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    init(theme: AppTheme = .saudi, onUnlockBonus: (() -> Void)?, onKeepColoring: @escaping () -> Void, onMorePictures: @escaping () -> Void) {
        self.theme = theme
        self.onUnlockBonus = onUnlockBonus
        self.onKeepColoring = onKeepColoring
        self.onMorePictures = onMorePictures
    }

    var body: some View {
        VStack(spacing: 0) {
            ZStack {
                theme.ground
                VStack(spacing: 0) {
                    Spacer(minLength: 0)
                    SaduBand().frame(height: 34)
                }
                FinishedStamp(theme: theme, size: 132)
                    .rotationEffect(.degrees(stamped ? -10 : -30))
                    .scaleEffect(stamped ? 1 : (reduceMotion ? 1 : 1.9))
                    .opacity(stamped ? 1 : 0)
                    .offset(y: -10)
            }
            .frame(height: 210)

            VStack(spacing: 22) {
                Text("You did it!")
                    .font(.system(size: 46, weight: .heavy, design: .rounded))
                    .foregroundStyle(theme.ink)
                VStack(spacing: 12) {
                    if let onUnlockBonus {
                        big("Get more colours", systemImage: "paintpalette.fill", fill: theme.accent, text: theme.onAccent, action: onUnlockBonus)
                    }
                    big("Keep coloring", systemImage: "paintbrush.fill", fill: theme.ground, text: .white, action: onKeepColoring)
                    big("More pictures", systemImage: "square.grid.2x2.fill", fill: theme.ink.opacity(0.08), text: theme.ink, action: onMorePictures)
                }
            }
            .padding(.horizontal, 36)
            .padding(.top, 26)
            .padding(.bottom, 34)
        }
        .frame(maxWidth: 460)
        .background(theme.tint)
        .clipShape(RoundedRectangle(cornerRadius: 34, style: .continuous))
        .shadow(color: .black.opacity(0.25), radius: 30, y: 14)
        .padding()
        .onAppear {
            withAnimation(reduceMotion ? .easeOut(duration: 0.2) : .spring(duration: 0.45, bounce: 0.45).delay(0.15)) {
                stamped = true
            }
        }
        .sensoryFeedback(.success, trigger: stamped)
    }

    private func big(_ title: LocalizedStringKey, systemImage: String, fill: Color, text: Color, action: @escaping () -> Void) -> some View {
        Button(action: action) {
            Label(title, systemImage: systemImage)
                .font(.title2.bold())
                .fontDesign(.rounded)
                .foregroundStyle(text)
                .frame(maxWidth: .infinity, minHeight: 64)
                .background(fill, in: Capsule())
                .contentShape(Capsule())
        }
        .buttonStyle(CelebrationButtonStyle())
    }
}

private struct CelebrationButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .scaleEffect(configuration.isPressed ? 0.96 : 1)
            .animation(.easeOut(duration: 0.15), value: configuration.isPressed)
    }
}

#Preview {
    CelebrationView(onUnlockBonus: {}, onKeepColoring: {}, onMorePictures: {})
}
