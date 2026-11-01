import SwiftUI

/// One page with its two modes over one ColoringState: Fill (tap a shape) and Freestyle (brush).
struct CanvasView: View {
    @Environment(AppEnvironment.self) private var env
    @Environment(\.dismiss) private var dismiss
    @Environment(\.horizontalSizeClass) private var sizeClass
    let region: Region
    let scene: ColoringScene

    @State private var state: ColoringState
    @State private var mode: ColoringMode = .fill
    @State private var color = ColorTray.crayons[0]
    @State private var brushSize: BrushSize = .medium
    @State private var page: LoadedPage?
    @State private var image: CGImage?
    @State private var loadFailed = false
    @State private var renderTask: Task<Void, Never>?
    @State private var showCelebration = false
    @State private var showGate = false
    @State private var gatePassed = false

    /// Everything decoded once per page.
    private struct LoadedPage {
        let assets: SceneAssets
        let renderer: CanvasRenderer
        let regionIds: Set<UInt32>
    }

    init(region: Region, scene: ColoringScene) {
        self.region = region
        self.scene = scene
        _state = State(initialValue: ColoringState(document: ColoringDocument(regionId: region.id, sceneId: scene.id, mode: .fill)))
    }

    var body: some View {
        VStack(spacing: 0) {
            controls
                .padding(.horizontal)
                .padding(.vertical, 12)

            pageArea
                .frame(maxWidth: .infinity, maxHeight: .infinity)

            tray
        }
        .background(theme.tint.ignoresSafeArea())
        .navigationTitle(scene.title)
        .navigationBarTitleDisplayMode(.inline)
        .toolbarBackground(theme.ground, for: .navigationBar)
        .toolbarBackground(.visible, for: .navigationBar)
        .toolbarColorScheme(.dark, for: .navigationBar)
        .overlay {
            if showCelebration {
                ZStack {
                    Color.black.opacity(0.25).ignoresSafeArea()
                    CelebrationView(
                        theme: theme,
                        onUnlockBonus: celebrationUnlock,
                        onKeepColoring: { showCelebration = false },
                        onMorePictures: {
                            env.ads.showInterstitialIfEligible()
                            dismiss()
                        }
                    )
                }
                .transition(.opacity.combined(with: .scale(scale: 0.9)))
            }
        }
        .sheet(isPresented: $showGate, onDismiss: unlockBonusIfPassed) {
            ParentalGate { gatePassed = true }
        }
        .sensoryFeedback(.impact(weight: .light), trigger: state.document.updatedAt)
        .task { await load() }
        .onChange(of: state.document.updatedAt) { documentChanged() }
        .onChange(of: mode) { modeChanged() }
        .onDisappear { saveOnLeave() }
    }

    // MARK: Views

    private var theme: AppTheme { .saudi }

    /// The mode switch and the page actions: side by side on iPad, the actions under the switch on iPhone.
    @ViewBuilder
    private var controls: some View {
        let actions = PageActions(
            canUndo: state.canUndo, canRedo: state.canRedo, canReset: !state.document.isEmpty,
            onUndo: { state.dispatch(.undo) }, onRedo: { state.dispatch(.redo) }, onReset: { state.dispatch(.reset) },
            theme: theme)
        if sizeClass == .compact {
            VStack(spacing: 10) {
                ModeSwitch(mode: $mode, theme: theme)
                actions
            }
        } else {
            HStack(spacing: 16) {
                ModeSwitch(mode: $mode, theme: theme)
                    .frame(maxWidth: 640)
                actions
            }
            .frame(maxWidth: .infinity)
        }
    }

    @ViewBuilder
    private var pageArea: some View {
        if let image, let page {
            PageView(
                image: image,
                isDrawing: mode == .freestyle,
                brushColor: color,
                brushWidth: brushSize.rawValue,
                onTap: { point, tolerance in tap(at: point, tolerance: tolerance, page: page) },
                onStroke: { points in stroke(points) }
            )
            .padding([.horizontal, .bottom])
        } else if loadFailed {
            ContentUnavailableView(scene.title, systemImage: "exclamationmark.triangle", description: Text("This picture could not be opened."))
        } else {
            ProgressView().controlSize(.large)
        }
    }

    /// The trays sit on plain paper so colours read true, under a thin strip of Sadu.
    @ViewBuilder
    private var tray: some View {
        if page != nil {
            VStack(spacing: 0) {
                SaduBand()
                    .frame(height: 12)
                trayContent
                    .frame(maxWidth: .infinity)
            }
            .background(Color(uiColor: .systemBackground).ignoresSafeArea(edges: .bottom))
        }
    }

    @ViewBuilder
    private var trayContent: some View {
        if let page {
            let suggested = page.assets.palette.swatches.map(\.color)
            let bonus = env.rewards.bonusColorsUnlocked ? ColorTray.bonusColors : []
            switch mode {
            case .fill:
                ColorTray(suggested: suggested, selection: $color, bonus: bonus, onUnlockBonus: unlockBonus)
            case .freestyle:
                // On a phone the brush sizes get their own row, so the colours keep the full width.
                if sizeClass == .compact {
                    VStack(spacing: 0) {
                        BrushSizePicker(size: $brushSize, color: color, theme: theme)
                            .padding(.top, 6)
                        ColorTray(suggested: suggested, selection: $color, bonus: bonus, onUnlockBonus: unlockBonus)
                    }
                } else {
                    HStack(spacing: 0) {
                        BrushSizePicker(size: $brushSize, color: color, theme: theme)
                        Divider().frame(height: 48)
                        ColorTray(suggested: suggested, selection: $color, bonus: bonus, onUnlockBonus: unlockBonus)
                    }
                }
            }
        }
    }

    /// Opens the parental gate for the bonus colours; nil once they are unlocked.
    private var unlockBonus: (() -> Void)? {
        guard !env.rewards.bonusColorsUnlocked else { return nil }
        return { showGate = true }
    }

    private var celebrationUnlock: (() -> Void)? {
        guard !env.rewards.bonusColorsUnlocked else { return nil }
        return {
            showCelebration = false
            showGate = true
        }
    }

    // MARK: Touches

    private func tap(at point: CGPoint, tolerance: Int, page: LoadedPage) {
        switch mode {
        case .fill:
            FillTool(map: page.assets.map, color: color, tolerance: tolerance).began(at: point, state: state)
        case .freestyle:
            break
        }
    }

    private func stroke(_ points: [CGPoint]) {
        guard let first = points.first else { return }
        let brush = BrushTool(color: color, width: brushSize.rawValue)
        brush.began(at: first, state: state)
        points.dropFirst().forEach { brush.moved(to: $0, state: state) }
        brush.ended(at: points.last ?? first, state: state)
    }

    // MARK: Document

    private func documentChanged() {
        rerender()
        checkCompletion()
        try? env.persistence.save(state.document)
    }

    private func modeChanged() {
        state.setMode(mode)
    }

    private func checkCompletion() {
        guard let page, state.document.completedAt == nil else { return }
        let finished: Bool
        switch mode {
        case .fill: finished = FillTool.isComplete(regionIds: page.regionIds, document: state.document)
        case .freestyle: finished = false
        }
        guard finished else { return }
        state.markCompleted()
        try? env.persistence.save(state.document)
        withAnimation(.spring(duration: 0.4)) { showCelebration = true }
    }

    private func unlockBonusIfPassed() {
        guard gatePassed else { return }
        gatePassed = false
        let rewards = env.rewards
        if env.ads.isRewardedAvailable {
            env.ads.showRewarded { DispatchQueue.main.async { rewards.unlockBonusColors() } }
        } else {
            rewards.unlockBonusColors()
        }
    }

    // MARK: Loading and drawing

    /// Decodes the scene off the main thread, restores saved progress, then draws.
    private func load() async {
        guard page == nil else { return }
        let regionId = region.id, sceneId = scene.id
        let loaded = await Task.detached(priority: .userInitiated) { () -> LoadedPage? in
            guard let assets = try? SceneAssets.load(regionId: regionId, sceneId: sceneId) else { return nil }
            return LoadedPage(assets: assets, renderer: CanvasRenderer(map: assets.map), regionIds: assets.map.regionIds)
        }.value
        guard let loaded else {
            loadFailed = true
            return
        }
        if let first = loaded.assets.palette.swatches.first {
            color = first.color
        }
        page = loaded
        if let saved = env.persistence.load(regionId: regionId, sceneId: sceneId) {
            state = ColoringState(document: saved)
            mode = saved.mode
        }
        rerender()
    }

    /// Renders the current document off the main thread; a newer edit cancels an older render.
    private func rerender() {
        guard let page else { return }
        let renderer = page.renderer
        let document = state.document
        renderTask?.cancel()
        renderTask = Task {
            let rendered = await Task.detached(priority: .userInitiated) { renderer.render(document) }.value
            guard !Task.isCancelled else { return }
            image = rendered
        }
    }

    /// Saves progress and a gallery thumbnail of the page as it is now.
    private func saveOnLeave() {
        // Only after load: saving earlier would overwrite saved progress with a blank page.
        guard let page else { return }
        let document = state.document
        let persistence = env.persistence
        let environment = env
        try? persistence.save(document)
        let renderer = page.renderer
        Task.detached(priority: .utility) {
            if document.isEmpty {
                persistence.delete(regionId: document.regionId, sceneId: document.sceneId)
            } else if let image = renderer.render(document), let png = CanvasRenderer.thumbnailPNG(of: image) {
                try? persistence.saveThumbnail(png, regionId: document.regionId, sceneId: document.sceneId)
            }
            await MainActor.run { environment.libraryVersion += 1 }
        }
    }
}
