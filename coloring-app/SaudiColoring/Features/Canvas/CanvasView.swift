import SwiftUI

/// Hosts the three modes over one ColoringState. Mode-specific UI lives in
/// Fill/, Freestyle/ and PaintByNumber/ subfolders. Fill is playable; the other two come next.
struct CanvasView: View {
    @Environment(AppEnvironment.self) private var env
    let region: Region
    let scene: ColoringScene

    @State private var state: ColoringState
    @State private var mode: ColoringMode = .fill
    @State private var color = ColorTray.crayons[0]
    @State private var assets: SceneAssets?
    @State private var renderer: CanvasRenderer?
    @State private var image: CGImage?
    @State private var loadFailed = false
    @State private var renderTask: Task<Void, Never>?

    init(region: Region, scene: ColoringScene) {
        self.region = region
        self.scene = scene
        _state = State(initialValue: ColoringState(document: ColoringDocument(regionId: region.id, sceneId: scene.id, mode: .fill)))
    }

    var body: some View {
        VStack(spacing: 0) {
            Picker("Mode", selection: $mode) {
                Label("Fill", systemImage: "drop.fill").tag(ColoringMode.fill)
                Label("Paint", systemImage: "paintbrush.pointed.fill").tag(ColoringMode.freestyle)
                Label("Numbers", systemImage: "number.square.fill").tag(ColoringMode.paintByNumber)
            }
            .pickerStyle(.segmented)
            .padding()

            canvas
                .padding([.horizontal, .bottom])
                .frame(maxWidth: .infinity, maxHeight: .infinity)

            if mode == .fill, let assets {
                ColorTray(suggested: assets.palette.swatches.map(\.color), selection: $color)
            }
        }
        .navigationTitle(scene.title)
        .toolbar {
            Button("Undo", systemImage: "arrow.uturn.backward") { state.dispatch(.undo) }.disabled(!state.canUndo)
            Button("Redo", systemImage: "arrow.uturn.forward") { state.dispatch(.redo) }.disabled(!state.canRedo)
        }
        .sensoryFeedback(.impact(weight: .light), trigger: state.document.updatedAt)
        .task { await load() }
        .onChange(of: state.document.updatedAt) {
            rerender()
            try? env.persistence.save(state.document)
        }
        .onDisappear {
            // Only after load: saving earlier would overwrite saved progress with a blank page.
            if assets != nil { try? env.persistence.save(state.document) }
        }
    }

    @ViewBuilder
    private var canvas: some View {
        if let image, let assets {
            FillCanvas(image: image) { point, tolerance in
                guard mode == .fill else { return }
                FillTool(map: assets.map, color: color, tolerance: tolerance).began(at: point, state: state)
            }
            .overlay(alignment: .top) {
                if mode != .fill {
                    Label("Coming soon", systemImage: "sparkles")
                        .font(.title2.bold())
                        .padding()
                        .background(.thinMaterial, in: Capsule())
                        .padding()
                }
            }
        } else if loadFailed {
            ContentUnavailableView(scene.title, systemImage: "exclamationmark.triangle", description: Text("This picture could not be opened."))
        } else {
            ProgressView().controlSize(.large)
        }
    }

    /// Decodes the scene off the main thread, restores saved progress, then draws.
    private func load() async {
        guard assets == nil else { return }
        let regionId = region.id, sceneId = scene.id
        let loaded = await Task.detached(priority: .userInitiated) { () -> (SceneAssets, CanvasRenderer)? in
            guard let assets = try? SceneAssets.load(regionId: regionId, sceneId: sceneId) else { return nil }
            return (assets, CanvasRenderer(map: assets.map))
        }.value
        guard let loaded else {
            loadFailed = true
            return
        }
        let (assets, renderer) = loaded
        if let saved = env.persistence.load(regionId: regionId, sceneId: sceneId) {
            state = ColoringState(document: saved)
        }
        if let first = assets.palette.swatches.first { color = first.color }
        self.assets = assets
        self.renderer = renderer
        rerender()
    }

    /// Renders the current document off the main thread; a newer edit cancels an older render.
    private func rerender() {
        guard let renderer else { return }
        let document = state.document
        renderTask?.cancel()
        renderTask = Task {
            let rendered = await Task.detached(priority: .userInitiated) { renderer.render(document) }.value
            guard !Task.isCancelled else { return }
            image = rendered
        }
    }
}
