import SwiftUI

/// Root screen: regions on the leading side (iPad sidebar), scenes of the selected region on the right.
struct HomeView: View {
    @Environment(AppEnvironment.self) private var env
    @State private var selectedRegion: Region?

    var body: some View {
        NavigationSplitView {
            List(env.catalog.regions, selection: $selectedRegion) { region in
                Label(region.name, systemImage: "map")
                    .font(.title2)
                    .frame(minHeight: 60)
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

#Preview(traits: .landscapeLeft) {
    HomeView().environment(AppEnvironment.preview())
}
