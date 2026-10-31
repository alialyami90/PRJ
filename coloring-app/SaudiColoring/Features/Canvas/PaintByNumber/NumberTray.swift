import SwiftUI

/// Paint by Number tray: one big numbered swatch per colour; a tick once that number is all painted.
struct NumberTray: View {
    let swatches: [Palette.Swatch]
    let finished: Set<Int>
    @Binding var selection: Int

    var body: some View {
        ScrollViewReader { proxy in
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: 12) {
                    ForEach(swatches, id: \.number) { swatch($0).id($0.number) }
                }
                .padding(.horizontal)
                .padding(.vertical, 8)
            }
            .onChange(of: selection) { proxy.scrollTo(selection, anchor: .center) }
        }
    }

    private func swatch(_ swatch: Palette.Swatch) -> some View {
        let isSelected = swatch.number == selection
        let isDone = finished.contains(swatch.number)
        let rgb = SceneColor.rgb(fromHex: swatch.color) ?? 0xFFFFFF
        // Light paint gets dark digits and the other way round.
        let luminance = 0.299 * Double(rgb >> 16 & 0xFF) + 0.587 * Double(rgb >> 8 & 0xFF) + 0.114 * Double(rgb & 0xFF)
        return Button {
            selection = swatch.number
        } label: {
            Circle()
                .fill(Color(hex: swatch.color))
                .overlay(Circle().strokeBorder(.black.opacity(0.25), lineWidth: 2))
                .overlay {
                    if isDone {
                        Image(systemName: "checkmark").font(.title2.bold())
                    } else {
                        Text("\(swatch.number)").font(.title2.bold())
                    }
                }
                .foregroundStyle(luminance > 150 ? Color.black : Color.white)
                .overlay(Circle().strokeBorder(.primary, lineWidth: isSelected ? 5 : 0).padding(-8))
                .frame(width: 60, height: 60)
                .scaleEffect(isSelected ? 1.1 : 1)
                .opacity(isDone && !isSelected ? 0.5 : 1)
                .animation(.spring(duration: 0.2), value: isSelected)
                .padding(8)
        }
        .buttonStyle(.plain)
        .accessibilityLabel(Text("Number \(swatch.number)"))
        .accessibilityAddTraits(isSelected ? .isSelected : [])
    }
}

#Preview {
    NumberTray(swatches: [.init(number: 1, color: "#7EC8E3"), .init(number: 2, color: "#2E2E2E")],
               finished: [2], selection: .constant(1))
}
