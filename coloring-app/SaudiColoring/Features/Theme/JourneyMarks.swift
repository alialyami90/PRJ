import SwiftUI

/// One diamond per page of a region, filled for each finished page. Readable without reading.
struct ProgressDiamonds: View {
    let finished: Int
    let total: Int
    var size: CGFloat = 10
    var filled: Color = .white
    /// Outlines for pages still to do; 60% white keeps them above 3:1 on the rail.
    var empty: Color = .white.opacity(0.6)

    var body: some View {
        HStack(spacing: size * 0.45) {
            ForEach(0..<total, id: \.self) { i in
                Rectangle()
                    .fill(i < finished ? filled : .clear)
                    .overlay(Rectangle().strokeBorder(i < finished ? filled : empty, lineWidth: max(1.5, size * 0.16)))
                    .frame(width: size * 0.72, height: size * 0.72)
                    .rotationEffect(.degrees(45))
                    .frame(width: size, height: size)
            }
        }
        .accessibilityElement()
        .accessibilityLabel(Text("\(finished) of \(total) pictures finished"))
    }
}

/// A stop on the journey rail: a hollow bead on the route that fills with gold, like a clock face,
/// as the region's pages are finished, and shows a star once all of them are.
struct RouteStop: View {
    var theme: AppTheme = .saudi
    /// Finished pages over all pages, 0 to 1.
    let progress: Double
    let isSelected: Bool
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    var body: some View {
        let size: CGFloat = isSelected ? 32 : 26
        let complete = progress >= 1
        ZStack {
            Circle().fill(Shell.rail)
            if complete {
                Circle().fill(theme.accent)
            } else if progress > 0 {
                // A pie wedge: a stroke as wide as the radius, trimmed to the progress.
                Circle()
                    .trim(from: 0, to: progress)
                    .stroke(theme.accent, lineWidth: size / 2)
                    .rotationEffect(.degrees(-90))
                    .padding(size / 4)
            }
            Circle().strokeBorder(complete || progress > 0 ? theme.accent : .white.opacity(0.85), lineWidth: 3)
            if complete {
                Image(systemName: "star.fill")
                    .font(.system(size: size * 0.42, weight: .bold))
                    .foregroundStyle(theme.onAccent)
            }
        }
        .overlay(Circle().strokeBorder(.white, lineWidth: isSelected ? 2 : 0).padding(-3))
        .frame(width: size, height: size)
        .shadow(color: .black.opacity(0.25), radius: 3, y: 2)
        .animation(reduceMotion ? nil : .spring(duration: 0.3), value: isSelected)
        .accessibilityHidden(true)
    }
}

/// The stamp on a finished page: a round green seal with a gold stitched ring and a star.
struct FinishedStamp: View {
    var theme: AppTheme = .saudi
    var size: CGFloat = 64

    var body: some View {
        ZStack {
            Circle().fill(theme.ground)
            Circle()
                .strokeBorder(theme.accent, style: StrokeStyle(lineWidth: max(2, size * 0.05), dash: [size * 0.07, size * 0.05]))
                .padding(size * 0.09)
            Circle()
                .fill(.white)
                .padding(size * 0.22)
            Image(systemName: "star.fill")
                .font(.system(size: size * 0.3, weight: .black))
                .foregroundStyle(theme.ground)
        }
        .frame(width: size, height: size)
        .overlay(Circle().strokeBorder(.white, lineWidth: max(2, size * 0.05)))
        .shadow(color: .black.opacity(0.22), radius: size * 0.08, y: size * 0.04)
        .accessibilityElement()
        .accessibilityLabel(Text("Finished"))
    }
}

#Preview {
    HStack(spacing: 24) {
        FinishedStamp()
        RouteStop(progress: 1, isSelected: true)
        RouteStop(progress: 0.375, isSelected: false)
        ProgressDiamonds(finished: 3, total: 8, filled: .black, empty: .gray)
    }
    .padding()
}
