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
                        .background(option == size ? Color.accentColor.opacity(0.2) : .clear, in: RoundedRectangle(cornerRadius: 14))
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
