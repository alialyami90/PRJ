import SwiftUI

/// Hosts the three modes over one ColoringState. Mode-specific UI lives in
/// Fill/, Freestyle/ and PaintByNumber/ subfolders.
struct CanvasView: View {
    @Environment(AppEnvironment.self) private var env
    let region: Region
    let scene: ColoringScene

    @State private var state: ColoringState
    @State private var mode: ColoringMode = .fill

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

            // TODO: CanvasRenderer-backed drawing surface + colour tray
            ContentUnavailableView(scene.title, systemImage: "paintpalette", description: Text("Canvas coming in M1"))
        }
        .navigationTitle(scene.title)
        .toolbar {
            Button("Undo", systemImage: "arrow.uturn.backward") { state.dispatch(.undo) }.disabled(!state.canUndo)
            Button("Redo", systemImage: "arrow.uturn.forward") { state.dispatch(.redo) }.disabled(!state.canRedo)
        }
        .onDisappear { try? env.persistence.save(state.document) }
    }
}
