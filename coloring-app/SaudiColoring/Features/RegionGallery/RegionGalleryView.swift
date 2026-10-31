import SwiftUI

/// The pages of one region: the child's own colouring once started, the line art before, a stamp once finished.
struct RegionGalleryView: View {
    @Environment(AppEnvironment.self) private var env
    let region: Region
    private let columns = [GridItem(.adaptive(minimum: 240), spacing: 28)]

    init(region: Region) {
        self.region = region
    }

    var body: some View {
        let theme = AppTheme.saudi
        ScrollView {
            VStack(spacing: 0) {
                RegionHeader(region: region, finished: env.finishedCount(in: region))
                LazyVGrid(columns: columns, spacing: 32) {
                    ForEach(region.scenes) { scene in
                        NavigationLink(value: scene) {
                            SceneCard(region: region, scene: scene)
                        }
                        .buttonStyle(CardButtonStyle())
                    }
                }
                .padding(.horizontal, 28)
                .padding(.top, 28)
                .padding(.bottom, 40)
            }
        }
        .background(theme.tint.ignoresSafeArea())
        .navigationTitle(region.shortName)
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            // The header below carries the name; the bar stays a plain band of the region's colour.
            ToolbarItem(placement: .principal) { Color.clear.frame(width: 1, height: 1) }
        }
        .toolbarBackground(theme.ground, for: .navigationBar)
        .toolbarBackground(.visible, for: .navigationBar)
        .toolbarColorScheme(.dark, for: .navigationBar)
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

/// The region's name in both languages on the green band, how far the child has got, and the Sadu band beneath.
private struct RegionHeader: View {
    let region: Region
    let finished: Int
    @ScaledMetric(relativeTo: .largeTitle) private var titleSize: CGFloat = 50

    var body: some View {
        let theme = AppTheme.saudi
        VStack(spacing: 0) {
            HStack(alignment: .center, spacing: 20) {
                VStack(alignment: .leading, spacing: 4) {
                    Text(region.shortName)
                        .font(.system(size: titleSize, weight: .heavy, design: .rounded))
                        .lineLimit(1)
                        .minimumScaleFactor(0.6)
                    if let area = region.area {
                        Text(area)
                            .font(.title3.weight(.semibold))
                            .foregroundStyle(.white.opacity(0.82))
                    }
                }
                Spacer(minLength: 12)
                if !region.nameAr.isEmpty {
                    Text(region.shortNameAr)
                        .font(.system(size: titleSize * 0.82, weight: .bold, design: .rounded))
                        .lineLimit(1)
                        .minimumScaleFactor(0.5)
                }
            }
            HStack(spacing: 12) {
                ProgressDiamonds(finished: finished, total: region.scenes.count, size: 18, filled: .white, empty: .white.opacity(0.45))
                Text("\(finished) of \(region.scenes.count) done")
                    .font(.headline)
                    .foregroundStyle(.white.opacity(0.9))
                Spacer()
            }
            .accessibilityElement(children: .combine)
            .padding(.top, 14)
        }
        .foregroundStyle(.white)
        .padding(.horizontal, 28)
        .padding(.top, 8)
        .padding(.bottom, 22)
        .background(theme.ground)
        .overlay(alignment: .bottom) {
            SaduBand()
                .frame(height: 30)
                .offset(y: 30)
        }
        .padding(.bottom, 30)
    }
}

/// Lifts a little under the finger.
private struct CardButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .scaleEffect(configuration.isPressed ? 0.96 : 1)
            .animation(.spring(duration: 0.25, bounce: 0.4), value: configuration.isPressed)
    }
}

private struct SceneCard: View {
    @Environment(AppEnvironment.self) private var env
    let region: Region
    let scene: ColoringScene

    var body: some View {
        // Reading libraryVersion redraws the card after the canvas saves a new thumbnail.
        let _ = env.libraryVersion
        let theme = AppTheme.saudi
        let document = env.persistence.load(regionId: region.id, sceneId: scene.id)
        VStack(alignment: .leading, spacing: 10) {
            thumbnail(theme)
                .aspectRatio(4 / 3, contentMode: .fit)
                .frame(maxWidth: .infinity)
                .background(.white)
                .clipShape(RoundedRectangle(cornerRadius: 18, style: .continuous))
                .overlay(RoundedRectangle(cornerRadius: 18, style: .continuous).strokeBorder(theme.ink.opacity(0.8), lineWidth: 2.5))
                .shadow(color: theme.ink.opacity(0.16), radius: 10, y: 6)
                .overlay(alignment: .topTrailing) {
                    if document?.completedAt != nil {
                        FinishedStamp(theme: theme, size: 60)
                            .rotationEffect(.degrees(-12))
                            .offset(x: 12, y: -14)
                    }
                }
            Text(scene.title)
                .font(.headline)
                .fontDesign(.rounded)
                .foregroundStyle(theme.ink)
                .multilineTextAlignment(.leading)
                .lineLimit(2, reservesSpace: true)
        }
    }

    @ViewBuilder
    private func thumbnail(_ theme: AppTheme) -> some View {
        if let data = env.persistence.thumbnail(regionId: region.id, sceneId: scene.id), let image = UIImage(data: data) {
            Image(uiImage: image).resizable().scaledToFit()
        } else if let image = BundleImages.thumbnail(regionId: region.id, sceneId: scene.id) {
            Image(uiImage: image).resizable().scaledToFit()
        } else {
            Image(systemName: "paintpalette").font(.largeTitle)
                .foregroundStyle(theme.ground)
                .frame(maxWidth: .infinity, maxHeight: .infinity)
                .background(theme.tint)
        }
    }
}

#Preview(traits: .landscapeLeft) {
    NavigationStack {
        RegionGalleryView(region: SceneCatalog.sample.regions[0])
    }
    .environment(AppEnvironment.preview())
}
