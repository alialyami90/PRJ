import SwiftUI

/// Brush sizes in image pixels (a page is 2048 wide).
enum BrushSize: Double, CaseIterable, Identifiable {
    case small = 16, medium = 36, large = 72

    var id: Double { rawValue }

    /// Dot size in the picker, in points.
    var dot: CGFloat {
        switch self {
        case .small: 12
        case .medium: 22
        case .large: 36
        }
    }

    var name: LocalizedStringKey {
        switch self {
        case .small: "Thin brush"
        case .medium: "Medium brush"
        case .large: "Thick brush"
        }
    }
}

/// Three big dots for the brush size, shown next to the colours in Freestyle.
struct BrushSizePicker: View {
    @Binding var size: BrushSize
    let color: String
    var theme: AppTheme = .saudi

    var body: some View {
        HStack(spacing: 8) {
            ForEach(BrushSize.allCases) { option in
                Button {
                    size = option
                } label: {
                    Circle()
                        .fill(Color(hex: color))
                        .overlay(Circle().strokeBorder(.black.opacity(0.25), lineWidth: 1))
                        .frame(width: option.dot, height: option.dot)
                        .frame(width: 60, height: 60)
                        .background(option == size ? theme.tint : .clear, in: RoundedRectangle(cornerRadius: 16, style: .continuous))
                        .overlay(RoundedRectangle(cornerRadius: 16, style: .continuous)
                            .strokeBorder(option == size ? theme.ground : .clear, lineWidth: 2.5))
                }
                .buttonStyle(.plain)
                .accessibilityLabel(Text(option.name))
                .accessibilityAddTraits(option == size ? .isSelected : [])
            }
        }
        .padding(.horizontal)
    }
}

#Preview {
    BrushSizePicker(size: .constant(.medium), color: "#E53935")
}
