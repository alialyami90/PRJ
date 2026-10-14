import SwiftUI

/// Root screen: regions on the leading side (iPad sidebar), scenes of the selected region on the right.
struct HomeView: View {
    @Environment(AppEnvironment.self) private var env
    @State private var selectedRegion: Region?

    var body: some View {
        NavigationSplitView {
            List(env.catalog.regions, selection: $selectedRegion) { region in
                RegionRow(region: region)
                    .tag(region)
            }
            .navigationTitle("Saudi Colors")
        } detail: {
            if let region = selectedRegion ?? env.catalog.regions.first {
                // The gallery pushes the canvas, so the detail column needs its own stack.
                NavigationStack {
                    RegionGalleryView(region: region)
                }
                .id(region.id)
            } else {
                ContentUnavailableView("Pick a place", systemImage: "map")
            }
        }
    }
}

private struct RegionRow: View {
    let region: Region

    var body: some View {
        HStack(spacing: 16) {
            Group {
                if let cover = BundleImages.cover(regionId: region.id) {
                    Image(uiImage: cover).resizable().scaledToFill()
                } else {
                    Image(systemName: "map").font(.title).frame(maxWidth: .infinity, maxHeight: .infinity)
                        .background(.yellow.opacity(0.3))
                }
            }
            .frame(width: 96, height: 72)
            .clipShape(RoundedRectangle(cornerRadius: 12))
            Text(region.name)
                .font(.title3.bold())
        }
        .frame(minHeight: 80)
    }
}

#Preview(traits: .landscapeLeft) {
    HomeView().environment(AppEnvironment.preview())
}
