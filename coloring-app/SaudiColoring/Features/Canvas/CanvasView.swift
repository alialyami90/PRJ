import SwiftUI

/// One page with its two modes over one ColoringState: Fill (tap a shape) and Freestyle (brush).
struct CanvasView: View {
    @Environment(AppEnvironment.self) private var env
    @Environment(\.dismiss) private var dismiss
    @Environment(\.horizontalSizeClass) private var sizeClass
    @Environment(\.accessibilityReduceMotion) private var reduceMotion
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
    /// Whether the page counted as finished at the last render; nil until the first one.
    @State private var wasFinished: Bool?
    /// "You did it!" shows at most once per visit, so undoing and redoing the last shape cannot replay it.
    @State private var celebratedThisVisit = false
    /// The white shapes in gold, shown over the page when the child pauses near the end.
    @State private var hint: CGImage?
    @State private var hintTask: Task<Void, Never>?

    /// Everything decoded once per page.
    private struct LoadedPage {
        let assets: SceneAssets
        let renderer: CanvasRenderer
    }

    /// The finishing hint waits for this long without a change.
    private static let hintDelay: Duration = .seconds(5)
    /// It shows only once this much of the page has colour, to guide the finish rather than the start.
    private static let hintFrom = 0.7
    /// It points at this many of the biggest white shapes at a time.
    private static let hintShapes = 8
    /// Date gold (AppTheme.saudi.accent).
    private static let hintColor: UInt32 = 0xE2A63B

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
        // No scrim: the finished picture stays in full view above the card.
        .overlay(alignment: .bottom) {
            if showCelebration {
                CelebrationView(
                    theme: theme,
                    onKeepColoring: { setCelebration(false) },
                    // Straight back to the pictures: never an ad after a finished page.
                    onMorePictures: { dismiss() }
                )
                .transition(reduceMotion ? .opacity : .move(edge: .bottom).combined(with: .opacity))
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
                hint: hint,
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

    private func setCelebration(_ shown: Bool) {
        withAnimation(reduceMotion ? .easeOut(duration: 0.2) : .spring(duration: 0.4)) { showCelebration = shown }
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
        // Colouring on after "You did it!" puts the card away, like tapping Keep coloring.
        if showCelebration { setCelebration(false) }
        rerender()
        try? env.persistence.save(state.document)
    }

    private func modeChanged() {
        state.setMode(mode)
    }

    /// Called after each render, with what the brush coloured, in Fill and in Paint alike.
    private func pageRendered(_ rendered: CanvasRenderer.Rendered, document: ColoringDocument, page: LoadedPage) {
        let progress = PageProgress(areas: page.renderer.regionAreas, fills: document.fills, painted: rendered.painted)
        checkCompletion(progress)
        scheduleHint(progress, page: page)
    }

    /// Celebrates when the page becomes finished. A page never finished before also celebrates when it
    /// opens already finished (coloured before this rule, or nearly to the end).
    private func checkCompletion(_ progress: PageProgress) {
        let previously = wasFinished
        wasFinished = progress.isFinished
        guard progress.isFinished, !celebratedThisVisit else { return }
        // A page finished on an earlier visit celebrates again only when it is coloured to the end again.
        guard state.document.completedAt == nil || previously == false else { return }
        celebratedThisVisit = true
        hideHint()
        state.markCompleted()
        try? env.persistence.save(state.document)
        env.ads.pageFinished()
        setCelebration(true)
    }

    /// After a pause near the end, the biggest white shapes glow gold a few times. Any change starts over.
    private func scheduleHint(_ progress: PageProgress, page: LoadedPage) {
        hideHint()
        guard !progress.isFinished, progress.covered >= Self.hintFrom, !progress.whiteShapes.isEmpty else { return }
        let shapes = Set(progress.whiteShapes.prefix(Self.hintShapes))
        let renderer = page.renderer
        hintTask = Task {
            try? await Task.sleep(for: Self.hintDelay)
            guard !Task.isCancelled else { return }
            let color = Self.hintColor
            let image = await Task.detached(priority: .utility) { renderer.highlight(shapes, color: color) }.value
            guard let image else { return }
            for _ in 0..<3 {
                guard !Task.isCancelled, !showCelebration else { return }
                hint = image
                try? await Task.sleep(for: .seconds(2.6))
                guard !Task.isCancelled else { return }
                hint = nil
                try? await Task.sleep(for: .seconds(8))
            }
        }
    }

    private func hideHint() {
        hintTask?.cancel()
        hintTask = nil
        hint = nil
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
        // The only interstitial slot: between pages, as a new one opens, never after a finish.
        env.ads.showInterstitialIfEligible()
        let regionId = region.id, sceneId = scene.id
        let loaded = await Task.detached(priority: .userInitiated) { () -> LoadedPage? in
            guard let assets = try? SceneAssets.load(regionId: regionId, sceneId: sceneId) else { return nil }
            return LoadedPage(assets: assets, renderer: CanvasRenderer(map: assets.map))
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
            let rendered = await Task.detached(priority: .userInitiated) { renderer.renderPage(document) }.value
            guard !Task.isCancelled else { return }
            image = rendered.image
            pageRendered(rendered, document: document, page: page)
        }
    }

    /// Saves progress and a gallery thumbnail of the page as it is now.
    private func saveOnLeave() {
        hideHint()
        // Only after load: saving earlier would overwrite saved progress with a blank page.
        guard let page else { return }
        let document = state.document
        let persistence = env.persistence
        let environment = env
        try? persistence.save(document)
        let renderer = page.renderer
        Task.detached(priority: .utility) {
            // A blank page that was finished before keeps its file: the seal is still earned.
            if document.isEmpty, document.completedAt == nil {
                persistence.delete(regionId: document.regionId, sceneId: document.sceneId)
            } else if let image = renderer.render(document), let png = CanvasRenderer.thumbnailPNG(of: image) {
                try? persistence.saveThumbnail(png, regionId: document.regionId, sceneId: document.sceneId)
            }
            await MainActor.run { environment.libraryVersion += 1 }
        }
    }
}
