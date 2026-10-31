import SwiftUI

/// One diamond per page of a region, filled for each finished page. Readable without reading.
struct ProgressDiamonds: View {
    let finished: Int
    let total: Int
    var size: CGFloat = 10
    var filled: Color = .white
    var empty: Color = .white.opacity(0.35)

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

/// A stop on the journey rail: the region's colour, a star once every page is finished.
struct RouteStop: View {
    let theme: RegionTheme
    let complete: Bool
    let isSelected: Bool

    var body: some View {
        let size: CGFloat = isSelected ? 30 : 24
        Circle()
            .fill(theme.ground)
            .overlay(Circle().strokeBorder(.white, lineWidth: 3))
            .overlay {
                if complete {
                    Image(systemName: "star.fill")
                        .font(.system(size: size * 0.42, weight: .bold))
                        .foregroundStyle(.white)
                }
            }
            .frame(width: size, height: size)
            .shadow(color: .black.opacity(0.25), radius: 3, y: 2)
            .animation(.spring(duration: 0.3), value: isSelected)
            .accessibilityHidden(true)
    }
}

/// The region's stamp for a finished page: a round seal in the region's colours with a star.
struct RegionStamp: View {
    let theme: RegionTheme
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
        RegionStamp(theme: .of("asir"))
        RouteStop(theme: .of("jeddah"), complete: true, isSelected: true)
        ProgressDiamonds(finished: 3, total: 8, filled: .black, empty: .gray)
    }
    .padding()
}
