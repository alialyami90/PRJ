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

/// The regions as stops on one caravan route down the rail. The stretch between two regions the child
/// has finished pages in is drawn solid, as road already travelled; the rest stays dotted.
private struct JourneyRail: View {
    @Environment(AppEnvironment.self) private var env
    let regions: [Region]
    let selectedId: String?
    let onSelect: (Region) -> Void

    var body: some View {
        let finished = regions.map { env.finishedCount(in: $0) }
        let visited = finished.map { $0 > 0 }
        ScrollViewReader { proxy in
            ScrollView {
                VStack(spacing: 0) {
                    ForEach(Array(regions.enumerated()), id: \.element.id) { index, region in
                        Button {
                            onSelect(region)
                        } label: {
                            StopRow(region: region,
                                    finished: finished[index],
                                    lineAbove: index == 0 ? nil : (visited[index - 1] && visited[index]),
                                    lineBelow: index == regions.count - 1 ? nil : (visited[index] && visited[index + 1]),
                                    isSelected: region.id == selectedId)
                        }
                        .buttonStyle(StopButtonStyle())
                        .id(region.id)
                        .accessibilityLabel(Text(verbatim: region.displayName()))
                        .accessibilityValue(Text("\(finished[index]) of \(region.scenes.count) pictures finished"))
                        .accessibilityAddTraits(region.id == selectedId ? .isSelected : [])
                    }
                }
                .padding(.vertical, 8)
            }
            // Keep the child's current stop in view.
            .onAppear { if let selectedId { proxy.scrollTo(selectedId) } }
            .onChange(of: selectedId) { _, id in
                guard let id else { return }
                withAnimation(.easeInOut(duration: 0.3)) { proxy.scrollTo(id) }
            }
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
    /// The route into and out of this stop: nil at the ends, true where it is already travelled.
    let lineAbove: Bool?
    let lineBelow: Bool?
    let isSelected: Bool

    var body: some View {
        let theme = AppTheme.saudi
        HStack(spacing: 0) {
            ZStack {
                VStack(spacing: 0) {
                    RouteLine(travelled: lineAbove ?? false).opacity(lineAbove == nil ? 0 : 1)
                    RouteLine(travelled: lineBelow ?? false).opacity(lineBelow == nil ? 0 : 1)
                }
                RouteStop(progress: region.scenes.isEmpty ? 0 : Double(finished) / Double(region.scenes.count),
                          isSelected: isSelected)
            }
            .frame(width: 48)
            .frame(maxHeight: .infinity)

            HStack(spacing: 14) {
                cover(theme)
                VStack(alignment: .leading, spacing: 3) {
                    Text(verbatim: region.displayName())
                        .font(.title3.weight(.heavy))
                        .fontDesign(.rounded)
                        .foregroundStyle(Shell.railText)
                    subtitle
                        .font(.subheadline.weight(.semibold))
                        .foregroundStyle(Shell.railSecondary)
                    ProgressDiamonds(finished: finished, total: region.scenes.count, size: 14)
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

    /// "Najd · الرياض" (in Arabic, "نجد · Riyadh"): the area, then the name in the other language; on two
    /// lines when one is too narrow, so neither name wraps on its own.
    @ViewBuilder
    private var subtitle: some View {
        switch (region.displayArea(), region.otherName()) {
        case let (area?, other?):
            ViewThatFits(in: .horizontal) {
                Text(verbatim: "\(area) · \(other)").lineLimit(1)
                VStack(alignment: .leading, spacing: 1) {
                    Text(verbatim: area)
                    Text(verbatim: other)
                }
            }
        case let (area?, nil): Text(verbatim: area)
        case let (nil, other?): Text(verbatim: other)
        case (nil, nil): EmptyView()
        }
    }

    private func cover(_ theme: AppTheme) -> some View {
        Group {
            if let cover = BundleImages.cover(regionId: region.id) {
                Image(uiImage: cover).resizable().scaledToFill()
            } else {
                theme.tint.overlay(Image(systemName: "map").font(.title).foregroundStyle(theme.ground))
            }
        }
        .frame(width: 100, height: 75)
        .overlay(alignment: .bottom) {
            SaduBand().frame(height: 10)
        }
        .clipShape(RoundedRectangle(cornerRadius: 14, style: .continuous))
        .overlay(RoundedRectangle(cornerRadius: 14, style: .continuous)
            .strokeBorder(.white.opacity(isSelected ? 1 : 0.25), lineWidth: isSelected ? 3 : 1))
        .accessibilityHidden(true)
    }
}

/// One stretch of the caravan route, top to bottom of its frame: solid once travelled, dotted ahead.
private struct RouteLine: View {
    let travelled: Bool

    var body: some View {
        VerticalLine()
            .stroke(Shell.route, style: travelled
                ? StrokeStyle(lineWidth: 5, lineCap: .butt)
                : StrokeStyle(lineWidth: 4, lineCap: .round, dash: [1, 10]))
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
