import SwiftUI

/// One page with its three modes over one ColoringState: Fill (tap a shape), Freestyle (brush)
/// and Paint by Number (each shape takes only the colour of its number).
struct CanvasView: View {
    @Environment(AppEnvironment.self) private var env
    @Environment(\.dismiss) private var dismiss
    let region: Region
    let scene: ColoringScene

    @State private var state: ColoringState
    @State private var mode: ColoringMode = .fill
    @State private var color = ColorTray.crayons[0]
    @State private var brushSize: BrushSize = .medium
    @State private var selectedNumber = 1
    @State private var page: LoadedPage?
    @State private var labels: [UInt32: RegionLabel]?
    @State private var computingLabels = false
    @State private var image: CGImage?
    @State private var loadFailed = false
    @State private var renderTask: Task<Void, Never>?
    @State private var showCelebration = false
    @State private var showGate = false
    @State private var gatePassed = false
    @State private var confirmReset = false
    /// "Try number 3" after a wrong Paint by Number tap.
    @State private var tryNumber: Int?
    @State private var tryNumberTask: Task<Void, Never>?

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
            ModeSwitch(mode: $mode, theme: theme)
                .padding(.horizontal)
                .padding(.vertical, 12)

            pageArea
                .frame(maxWidth: .infinity, maxHeight: .infinity)
                .overlay(alignment: .top) { tryNumberBubble }

            tray
        }
        .background(theme.tint.ignoresSafeArea())
        .navigationTitle(scene.title)
        .navigationBarTitleDisplayMode(.inline)
        .toolbarBackground(theme.ground, for: .navigationBar)
        .toolbarBackground(.visible, for: .navigationBar)
        .toolbarColorScheme(.dark, for: .navigationBar)
        .toolbar {
            ToolbarItemGroup(placement: .primaryAction) {
                Button("Undo", systemImage: "arrow.uturn.backward") { state.dispatch(.undo) }.disabled(!state.canUndo)
                Button("Redo", systemImage: "arrow.uturn.forward") { state.dispatch(.redo) }.disabled(!state.canRedo)
                Button("Start again", systemImage: "trash") { confirmReset = true }.disabled(state.document.isEmpty)
            }
        }
        .confirmationDialog("Start this picture again?", isPresented: $confirmReset, titleVisibility: .visible) {
            Button("Start again", role: .destructive) { state.dispatch(.reset) }
        }
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
        .onChange(of: selectedNumber) { if mode == .paintByNumber { rerender() } }
        .onDisappear { saveOnLeave() }
    }

    // MARK: Views

    private var theme: AppTheme { .saudi }

    @ViewBuilder
    private var pageArea: some View {
        if let image, let page {
            PageView(
                image: image,
                numbers: mode == .paintByNumber ? pageNumbers(page) : [],
                isDrawing: mode == .freestyle,
                brushColor: color,
                brushWidth: brushSize.rawValue,
                onTap: { point, tolerance in tap(at: point, tolerance: tolerance, page: page) },
                onStroke: { points in stroke(points) }
            )
            .padding([.horizontal, .bottom])
            .overlay {
                if mode == .paintByNumber, labels == nil {
                    ProgressView().controlSize(.large)
                }
            }
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
                HStack(spacing: 0) {
                    BrushSizePicker(size: $brushSize, color: color, theme: theme)
                    Divider().frame(height: 48)
                    ColorTray(suggested: suggested, selection: $color, bonus: bonus, onUnlockBonus: unlockBonus)
                }
            case .paintByNumber:
                NumberTray(swatches: page.assets.palette.swatches,
                           finished: numbersTool(page).finishedNumbers(state),
                           selection: $selectedNumber)
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

    @ViewBuilder
    private var tryNumberBubble: some View {
        if let tryNumber {
            Label("Try number \(tryNumber)", systemImage: "hand.point.up.left.fill")
                .font(.title2.bold())
                .fontDesign(.rounded)
                .foregroundStyle(.white)
                .padding(.horizontal, 22)
                .padding(.vertical, 12)
                .background(theme.ground, in: Capsule())
                .shadow(color: .black.opacity(0.2), radius: 8, y: 4)
                .padding(.top, 12)
                .transition(.move(edge: .top).combined(with: .opacity))
        }
    }

    // MARK: Touches

    private func numbersTool(_ page: LoadedPage, tolerance: Int = 0) -> PaintByNumberTool {
        PaintByNumberTool(map: page.assets.map, palette: page.assets.palette, selectedNumber: selectedNumber, tolerance: tolerance)
    }

    /// Numbers still to paint, at the deepest point of their shape.
    private func pageNumbers(_ page: LoadedPage) -> [PageNumber] {
        guard let labels else { return [] }
        return page.assets.palette.entries.compactMap { entry in
            guard state.document.fills[entry.regionId] != entry.color, let label = labels[entry.regionId] else { return nil }
            return PageNumber(regionId: entry.regionId, number: entry.number, label: label, isSelected: entry.number == selectedNumber)
        }
    }

    private func tap(at point: CGPoint, tolerance: Int, page: LoadedPage) {
        switch mode {
        case .fill:
            FillTool(map: page.assets.map, color: color, tolerance: tolerance).began(at: point, state: state)
        case .paintByNumber:
            switch numbersTool(page, tolerance: tolerance).tap(at: point, state: state) {
            case .correct:
                moveToUnfinishedNumber(page)
            case let .wrong(expected):
                showTryNumber(expected)
            case .ignored:
                break
            }
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

    /// When the selected number is all painted, jump to the next one that is not.
    private func moveToUnfinishedNumber(_ page: LoadedPage) {
        let finished = numbersTool(page).finishedNumbers(state)
        guard finished.contains(selectedNumber) else { return }
        let numbers = page.assets.palette.swatches.map(\.number).filter { !finished.contains($0) }
        if let next = numbers.first(where: { $0 > selectedNumber }) ?? numbers.first {
            selectedNumber = next
        }
    }

    private func showTryNumber(_ number: Int) {
        withAnimation(.spring(duration: 0.3)) { tryNumber = number }
        tryNumberTask?.cancel()
        tryNumberTask = Task {
            try? await Task.sleep(for: .seconds(1.5))
            guard !Task.isCancelled else { return }
            withAnimation { tryNumber = nil }
        }
    }

    // MARK: Document

    private func documentChanged() {
        rerender()
        checkCompletion()
        try? env.persistence.save(state.document)
    }

    private func modeChanged() {
        state.setMode(mode)
        if mode == .paintByNumber, let page {
            computeLabels(page)
            moveToUnfinishedNumber(page)
        }
        rerender()
    }

    private func checkCompletion() {
        guard let page, state.document.completedAt == nil else { return }
        let finished: Bool
        switch mode {
        case .fill: finished = FillTool.isComplete(regionIds: page.regionIds, document: state.document)
        case .paintByNumber: finished = numbersTool(page).isComplete(state)
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
            selectedNumber = first.number
        }
        page = loaded
        if let saved = env.persistence.load(regionId: regionId, sceneId: sceneId) {
            state = ColoringState(document: saved)
            mode = saved.mode // onChange(of: mode) prepares Paint by Number if needed
        }
        rerender()
    }

    /// Where each number goes; one pass over the map, done once and only if Paint by Number is used.
    private func computeLabels(_ page: LoadedPage) {
        guard labels == nil, !computingLabels else { return }
        computingLabels = true
        let map = page.assets.map
        Task {
            labels = await Task.detached(priority: .userInitiated) { map.labels() }.value
            computingLabels = false
        }
    }

    /// Renders the current document off the main thread; a newer edit cancels an older render.
    private func rerender() {
        guard let page else { return }
        let renderer = page.renderer
        let document = state.document
        // Paint by Number tints the shapes still waiting for the selected number.
        let highlight: Set<UInt32> = mode == .paintByNumber
            ? Set(numbersTool(page).remaining(number: selectedNumber, state).map(\.regionId))
            : []
        renderTask?.cancel()
        renderTask = Task {
            let rendered = await Task.detached(priority: .userInitiated) { renderer.render(document, highlight: highlight) }.value
            guard !Task.isCancelled else { return }
            image = rendered
        }
    }

    /// Saves progress and a gallery thumbnail of the page as it is now (without the number hints).
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
