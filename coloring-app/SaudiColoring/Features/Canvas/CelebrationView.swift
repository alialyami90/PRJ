import SwiftUI

/// Shown when a page is finished. It sits at the foot of the canvas with no scrim, so the child's own
/// picture stays in full view: the seal presses down beside "You did it!", then two big choices.
/// Nothing here sells anything; bonus colours live behind the grown-up lock in the colour tray.
struct CelebrationView: View {
    let theme: AppTheme
    let onKeepColoring: () -> Void
    let onMorePictures: () -> Void
    @State private var stamped = false
    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    @Environment(\.horizontalSizeClass) private var sizeClass

    init(theme: AppTheme = .saudi, onKeepColoring: @escaping () -> Void, onMorePictures: @escaping () -> Void) {
        self.theme = theme
        self.onKeepColoring = onKeepColoring
        self.onMorePictures = onMorePictures
    }

    private var wide: Bool { sizeClass != .compact }

    var body: some View {
        VStack(spacing: 0) {
            SaduBand().frame(height: 16)
            Group {
                if wide {
                    HStack(spacing: 28) {
                        seal(size: 118)
                        VStack(alignment: .leading, spacing: 16) {
                            title
                            HStack(spacing: 12) { buttons }
                        }
                    }
                } else {
                    VStack(spacing: 16) {
                        HStack(spacing: 16) {
                            seal(size: 84)
                            title
                        }
                        VStack(spacing: 12) { buttons }
                    }
                }
            }
            .padding(.horizontal, wide ? 32 : 20)
            .padding(.top, 20)
            .padding(.bottom, 24)
        }
        .frame(maxWidth: wide ? 760 : .infinity)
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

    private func seal(size: CGFloat) -> some View {
        FinishedStamp(theme: theme, size: size)
            .rotationEffect(.degrees(stamped ? -10 : -30))
            .scaleEffect(stamped ? 1 : (reduceMotion ? 1 : 1.9))
            .opacity(stamped ? 1 : 0)
            .accessibilityHidden(true)
    }

    private var title: some View {
        Text("You did it!")
            .font(.system(size: wide ? 46 : 36, weight: .heavy, design: .rounded))
            .foregroundStyle(theme.ink)
            .lineLimit(1)
            .minimumScaleFactor(0.6)
            .accessibilityAddTraits(.isHeader)
    }

    @ViewBuilder
    private var buttons: some View {
        big("Keep coloring", systemImage: "paintbrush.fill", fill: theme.ground, text: .white, action: onKeepColoring)
        big("More pictures", systemImage: "square.grid.2x2.fill", fill: theme.ink.opacity(0.08), text: theme.ink, action: onMorePictures)
    }

    private func big(_ title: LocalizedStringKey, systemImage: String, fill: Color, text: Color, action: @escaping () -> Void) -> some View {
        Button(action: action) {
            Label(title, systemImage: systemImage)
                .font(.title2.bold())
                .fontDesign(.rounded)
                .foregroundStyle(text)
                .lineLimit(1)
                .minimumScaleFactor(0.7)
                .padding(.horizontal, 20)
                .frame(maxWidth: .infinity, minHeight: 64)
                .background(fill, in: Capsule())
                .contentShape(Capsule())
        }
        .buttonStyle(CelebrationButtonStyle())
    }
}

private struct CelebrationButtonStyle: ButtonStyle {
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .scaleEffect(configuration.isPressed && !reduceMotion ? 0.96 : 1)
            .animation(.easeOut(duration: 0.15), value: configuration.isPressed)
    }
}

#Preview {
    CelebrationView(onKeepColoring: {}, onMorePictures: {})
}
