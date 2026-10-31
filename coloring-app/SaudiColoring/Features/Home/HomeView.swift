import SwiftUI

/// Root screen: the journey rail of regions on the leading side (iPad sidebar), the selected region's pages beside it.
/// On iPhone the rail comes first and a region opens over it.
struct HomeView: View {
    @Environment(AppEnvironment.self) private var env
    @State private var selectedRegionId: String?
    @State private var compactColumn = NavigationSplitViewColumn.sidebar

    private var currentRegion: Region? {
        env.catalog.regions.first { $0.id == selectedRegionId } ?? env.catalog.regions.first
    }

    var body: some View {
        NavigationSplitView(preferredCompactColumn: $compactColumn) {
            JourneyRail(regions: env.catalog.regions, selectedId: currentRegion?.id) { region in
                selectedRegionId = region.id
                compactColumn = .detail
            }
            .navigationTitle("Saudi Colors")
            .toolbarBackground(Shell.rail, for: .navigationBar)
            .toolbarBackground(.visible, for: .navigationBar)
            .toolbarColorScheme(.dark, for: .navigationBar)
            .navigationSplitViewColumnWidth(min: 300, ideal: 350, max: 420)
        } detail: {
            if let region = currentRegion {
                // The gallery pushes the canvas, so the detail column needs its own stack.
                NavigationStack {
                    RegionGalleryView(region: region)
                }
                .id(region.id)
            } else {
                ContentUnavailableView("Pick a place", systemImage: "map")
            }
        }
        .tint(Shell.rail)
    }
}

/// The regions as stops on one dashed caravan route down the rail.
private struct JourneyRail: View {
    @Environment(AppEnvironment.self) private var env
    let regions: [Region]
    let selectedId: String?
    let onSelect: (Region) -> Void

    var body: some View {
        ScrollView {
            VStack(spacing: 0) {
                ForEach(Array(regions.enumerated()), id: \.element.id) { index, region in
                    Button {
                        onSelect(region)
                    } label: {
                        StopRow(region: region,
                                finished: env.finishedCount(in: region),
                                isFirst: index == 0,
                                isLast: index == regions.count - 1,
                                isSelected: region.id == selectedId)
                    }
                    .buttonStyle(StopButtonStyle())
                    .accessibilityLabel(Text(region.shortName))
                    .accessibilityValue(Text("\(env.finishedCount(in: region)) of \(region.scenes.count) pictures finished"))
                    .accessibilityAddTraits(region.id == selectedId ? .isSelected : [])
                }
            }
            .padding(.vertical, 8)
        }
        .background(Shell.rail.ignoresSafeArea())
    }
}

/// Presses in slightly, so a small finger sees the tap land.
private struct StopButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .scaleEffect(configuration.isPressed ? 0.97 : 1)
            .animation(.easeOut(duration: 0.15), value: configuration.isPressed)
    }
}

private struct StopRow: View {
    let region: Region
    let finished: Int
    let isFirst: Bool
    let isLast: Bool
    let isSelected: Bool

    var body: some View {
        let theme = region.theme
        HStack(spacing: 0) {
            ZStack {
                VStack(spacing: 0) {
                    RouteLine().opacity(isFirst ? 0 : 1)
                    RouteLine().opacity(isLast ? 0 : 1)
                }
                RouteStop(theme: theme, complete: finished == region.scenes.count && finished > 0, isSelected: isSelected)
            }
            .frame(width: 48)
            .frame(maxHeight: .infinity)

            HStack(spacing: 14) {
                cover(theme)
                VStack(alignment: .leading, spacing: 3) {
                    Text(region.shortName)
                        .font(.title3.weight(.heavy))
                        .fontDesign(.rounded)
                        .foregroundStyle(Shell.railText)
                    if !region.nameAr.isEmpty || region.area != nil {
                        Text(subtitle)
                            .font(.subheadline.weight(.semibold))
                            .foregroundStyle(Shell.railSecondary)
                    }
                    ProgressDiamonds(finished: finished, total: region.scenes.count, size: 11)
                        .padding(.top, 5)
                }
                .lineLimit(2)
                .minimumScaleFactor(0.8)
                Spacer(minLength: 0)
            }
            .padding(.vertical, 13)
            .padding(.trailing, 14)
        }
        .fixedSize(horizontal: false, vertical: true)
        .background(alignment: .leading) {
            if isSelected {
                UnevenRoundedRectangle(topLeadingRadius: 0, bottomLeadingRadius: 0, bottomTrailingRadius: 22, topTrailingRadius: 22,
                                       style: .continuous)
                    .fill(Shell.railSelected)
                    .padding(.trailing, 10)
            }
        }
        .contentShape(Rectangle())
    }

    /// "Najd · الرياض": the area in brackets, then the Arabic name.
    private var subtitle: String {
        [region.area, region.nameAr.isEmpty ? nil : region.nameAr].compactMap { $0 }.joined(separator: " · ")
    }

    private func cover(_ theme: RegionTheme) -> some View {
        Group {
            if let cover = BundleImages.cover(regionId: region.id) {
                Image(uiImage: cover).resizable().scaledToFill()
            } else {
                theme.tint.overlay(Image(systemName: "map").font(.title).foregroundStyle(theme.ground))
            }
        }
        .frame(width: 100, height: 75)
        .overlay(alignment: .bottom) {
            MotifBand(theme: theme).frame(height: 12)
        }
        .clipShape(RoundedRectangle(cornerRadius: 14, style: .continuous))
        .overlay(RoundedRectangle(cornerRadius: 14, style: .continuous)
            .strokeBorder(.white.opacity(isSelected ? 1 : 0.25), lineWidth: isSelected ? 3 : 1))
        .accessibilityHidden(true)
    }
}

/// One stretch of the dashed caravan route, top to bottom of its frame.
private struct RouteLine: View {
    var body: some View {
        VerticalLine()
            .stroke(Shell.route, style: StrokeStyle(lineWidth: 4, lineCap: .round, dash: [1, 10]))
            .frame(maxHeight: .infinity)
    }
}

private struct VerticalLine: Shape {
    func path(in rect: CGRect) -> Path {
        var path = Path()
        path.move(to: CGPoint(x: rect.midX, y: rect.minY))
        path.addLine(to: CGPoint(x: rect.midX, y: rect.maxY))
        return path
    }
}

#Preview(traits: .landscapeLeft) {
    HomeView().environment(AppEnvironment.preview())
}
