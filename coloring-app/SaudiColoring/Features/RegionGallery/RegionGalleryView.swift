import SwiftUI

struct RegionGalleryView: View {
    let region: Region
    private let columns = [GridItem(.adaptive(minimum: 220), spacing: 24)]

    var body: some View {
        ScrollView {
            LazyVGrid(columns: columns, spacing: 24) {
                ForEach(region.scenes) { scene in
                    NavigationLink(value: scene) {
                        VStack {
                            RoundedRectangle(cornerRadius: 20)
                                .fill(.yellow.opacity(0.3))
                                .aspectRatio(4 / 3, contentMode: .fit)
                                .overlay(Image(systemName: "paintpalette").font(.largeTitle))
                            Text(scene.title).font(.headline)
                        }
                    }
                }
            }
            .padding()
        }
        .navigationTitle(region.name)
        .navigationDestination(for: ColoringScene.self) { scene in
            CanvasView(region: region, scene: scene)
        }
        // TODO: AdBannerView() pinned to the bottom when env.ads.isBannerAvailable
    }
}
