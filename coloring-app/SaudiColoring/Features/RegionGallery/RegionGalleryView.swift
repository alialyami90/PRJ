import SwiftUI

/// The pages of one region: the child's own colouring once started, the line art before.
struct RegionGalleryView: View {
    @Environment(AppEnvironment.self) private var env
    let region: Region
    private let columns = [GridItem(.adaptive(minimum: 240), spacing: 24)]

    init(region: Region) {
        self.region = region
    }

    var body: some View {
        ScrollView {
            LazyVGrid(columns: columns, spacing: 24) {
                ForEach(region.scenes) { scene in
                    NavigationLink(value: scene) {
                        SceneCard(region: region, scene: scene)
                    }
                    .buttonStyle(.plain)
                }
            }
            .padding()
        }
        .navigationTitle(region.name)
        .navigationDestination(for: ColoringScene.self) { scene in
            CanvasView(region: region, scene: scene)
        }
        .safeAreaInset(edge: .bottom) {
            if env.ads.isBannerAvailable {
                AdBannerView(ads: env.ads)
                    .frame(height: 50)
                    .frame(maxWidth: .infinity)
                    .background(.bar)
            }
        }
    }
}

private struct SceneCard: View {
    @Environment(AppEnvironment.self) private var env
    let region: Region
    let scene: ColoringScene

    var body: some View {
        // Reading libraryVersion redraws the card after the canvas saves a new thumbnail.
        let _ = env.libraryVersion
        let document = env.persistence.load(regionId: region.id, sceneId: scene.id)
        VStack(alignment: .leading, spacing: 8) {
            thumbnail
                .aspectRatio(4 / 3, contentMode: .fit)
                .frame(maxWidth: .infinity)
                .background(.white)
                .clipShape(RoundedRectangle(cornerRadius: 20))
                .overlay(RoundedRectangle(cornerRadius: 20).strokeBorder(.black.opacity(0.1), lineWidth: 1))
                .overlay(alignment: .topTrailing) {
                    if document?.completedAt != nil {
                        Image(systemName: "star.circle.fill")
                            .font(.system(size: 36))
                            .symbolRenderingMode(.multicolor)
                            .foregroundStyle(.yellow)
                            .padding(8)
                            .accessibilityLabel(Text("Finished"))
                    }
                }
                .shadow(color: .black.opacity(0.1), radius: 6, y: 3)
            Text(scene.title)
                .font(.headline)
                .lineLimit(2, reservesSpace: true)
        }
    }

    @ViewBuilder
    private var thumbnail: some View {
        if let data = env.persistence.thumbnail(regionId: region.id, sceneId: scene.id), let image = UIImage(data: data) {
            Image(uiImage: image).resizable().scaledToFit()
        } else if let image = BundleImages.thumbnail(regionId: region.id, sceneId: scene.id) {
            Image(uiImage: image).resizable().scaledToFit()
        } else {
            Image(systemName: "paintpalette").font(.largeTitle)
                .frame(maxWidth: .infinity, maxHeight: .infinity)
                .background(.yellow.opacity(0.3))
        }
    }
}
