import SwiftUI

/// Back to the pictures, Undo, Redo and Start again, as big buttons with a word under each icon, beside
/// the mode switch. Start again asks first. The tiles grow with Dynamic Type rather than shrinking the words.
struct PageActions: View {
    /// Back to the region's pictures; nil hides the tile.
    var onPictures: (() -> Void)?
    let canUndo: Bool
    let canRedo: Bool
    let canReset: Bool
    let onUndo: () -> Void
    let onRedo: () -> Void
    let onReset: () -> Void
    var theme: AppTheme = .saudi
    @State private var confirmReset = false

    var body: some View {
        HStack(spacing: 8) {
            if let onPictures {
                action("Pictures", systemImage: "square.grid.2x2.fill", enabled: true, perform: onPictures)
                    .padding(.trailing, 8)
            }
            action("Undo", systemImage: "arrow.uturn.backward", enabled: canUndo, perform: onUndo)
            action("Redo", systemImage: "arrow.uturn.forward", enabled: canRedo, perform: onRedo)
            action("Start again", systemImage: "arrow.counterclockwise", enabled: canReset) { confirmReset = true }
                .confirmationDialog("Start this picture again?", isPresented: $confirmReset, titleVisibility: .visible) {
                    Button("Start again", role: .destructive, action: onReset)
                }
        }
    }

    private func action(_ title: LocalizedStringKey, systemImage: String, enabled: Bool,
                        perform: @escaping () -> Void) -> some View {
        Button(action: perform) {
            VStack(spacing: 2) {
                Image(systemName: systemImage).font(.title3.weight(.bold))
                Text(title).font(.caption.weight(.bold)).lineLimit(1)
            }
            .fontDesign(.rounded)
            .foregroundStyle(theme.ink)
            .padding(.horizontal, 8)
            .padding(.vertical, 6)
            .frame(minWidth: 76, minHeight: 60)
            .background(Color(uiColor: .systemBackground), in: RoundedRectangle(cornerRadius: 18, style: .continuous))
            .overlay(RoundedRectangle(cornerRadius: 18, style: .continuous).strokeBorder(theme.ink.opacity(0.12), lineWidth: 1))
            .contentShape(RoundedRectangle(cornerRadius: 18, style: .continuous))
        }
        .buttonStyle(.plain)
        .disabled(!enabled)
        .opacity(enabled ? 1 : 0.4)
    }
}

#Preview {
    PageActions(canUndo: true, canRedo: false, canReset: true, onUndo: {}, onRedo: {}, onReset: {})
        .padding()
        .background(AppTheme.saudi.tint)
}
