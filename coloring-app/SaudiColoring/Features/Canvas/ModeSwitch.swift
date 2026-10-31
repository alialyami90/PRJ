import SwiftUI

/// The three ways to colour, as one segmented row sized for small fingers. The chosen one fills green.
struct ModeSwitch: View {
    @Binding var mode: ColoringMode
    var theme: AppTheme = .saudi
    @Namespace private var selection
    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    /// On a phone the icon sits above the word, so "Numbers" fits and the three parts stay equal.
    @Environment(\.horizontalSizeClass) private var sizeClass

    var body: some View {
        HStack(spacing: 4) {
            ForEach(ColoringMode.allCases, id: \.self) { option in
                let isSelected = option == mode
                Button {
                    withAnimation(reduceMotion ? nil : .spring(duration: 0.3, bounce: 0.2)) { mode = option }
                } label: {
                    label(option)
                        .fontDesign(.rounded)
                        .lineLimit(1)
                        .minimumScaleFactor(0.7)
                        .foregroundStyle(isSelected ? Color.white : theme.ink)
                        .frame(maxWidth: .infinity, minHeight: 60)
                        .background {
                            if isSelected {
                                Capsule()
                                    .fill(theme.ground)
                                    .shadow(color: theme.ground.opacity(0.35), radius: 6, y: 3)
                                    .matchedGeometryEffect(id: "selected", in: selection)
                            }
                        }
                        .contentShape(Capsule())
                }
                .buttonStyle(.plain)
                .accessibilityAddTraits(isSelected ? .isSelected : [])
            }
        }
        .padding(5)
        .background(Color(uiColor: .systemBackground), in: Capsule())
        .overlay(Capsule().strokeBorder(theme.ink.opacity(0.12), lineWidth: 1))
    }

    @ViewBuilder
    private func label(_ option: ColoringMode) -> some View {
        if sizeClass == .compact {
            VStack(spacing: 2) {
                Image(systemName: option.symbol).font(.title3.weight(.bold))
                Text(option.title).font(.subheadline.weight(.bold))
            }
            .padding(.vertical, 4)
        } else {
            Label(option.title, systemImage: option.symbol)
                .font(.title3.weight(.bold))
        }
    }
}

extension ColoringMode {
    var title: LocalizedStringKey {
        switch self {
        case .fill: "Fill"
        case .freestyle: "Paint"
        case .paintByNumber: "Numbers"
        }
    }

    var symbol: String {
        switch self {
        case .fill: "drop.fill"
        case .freestyle: "paintbrush.pointed.fill"
        case .paintByNumber: "number.square.fill"
        }
    }
}

#Preview {
    ModeSwitch(mode: .constant(.freestyle)).padding()
}
