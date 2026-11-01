import Foundation
import Observation

/// Every user interaction on the canvas is an action; views dispatch and never mutate directly.
enum ColoringAction {
    case fill(regionId: UInt32, color: String)
    case stroke(Stroke)
    case clearRegion(UInt32)
    case undo
    case redo
    case reset
}

@Observable
final class ColoringState {
    private(set) var document: ColoringDocument
    private var undoStack: [ColoringDocument] = []
    private var redoStack: [ColoringDocument] = []

    init(document: ColoringDocument) {
        self.document = document
    }

    var canUndo: Bool { !undoStack.isEmpty }
    var canRedo: Bool { !redoStack.isEmpty }

    func dispatch(_ action: ColoringAction) {
        switch action {
        case .undo:
            guard let previous = undoStack.popLast() else { return }
            redoStack.append(document)
            restore(previous)
        case .redo:
            guard let next = redoStack.popLast() else { return }
            undoStack.append(document)
            restore(next)
        default:
            undoStack.append(document)
            redoStack.removeAll()
            apply(action)
        }
        document.updatedAt = .now
    }

    /// Which mode the child last used on this page; not an undo step.
    func setMode(_ mode: ColoringMode) {
        document.mode = mode
    }

    /// Records that the page was finished, once; not an undo step. A finished page stays earned:
    /// undo, redo and Start again never take the mark away.
    func markCompleted(at date: Date = .now) {
        guard document.completedAt == nil else { return }
        document.completedAt = date
    }

    /// Undo and redo step through the drawing only; the mode and the finished mark stay as they are now.
    private func restore(_ snapshot: ColoringDocument) {
        var restored = snapshot
        restored.mode = document.mode
        restored.completedAt = document.completedAt ?? snapshot.completedAt
        document = restored
    }

    private func apply(_ action: ColoringAction) {
        switch action {
        case let .fill(regionId, color): document.fills[regionId] = color
        case let .stroke(stroke): document.strokes.append(stroke)
        case let .clearRegion(regionId): document.fills.removeValue(forKey: regionId)
        case .reset:
            // Start again clears the picture, not the seal the child earned for it.
            document.fills.removeAll()
            document.strokes.removeAll()
        case .undo, .redo: break
        }
    }
}
