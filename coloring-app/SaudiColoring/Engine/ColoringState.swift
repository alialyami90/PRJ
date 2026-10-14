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
            document = previous
        case .redo:
            guard let next = redoStack.popLast() else { return }
            undoStack.append(document)
            document = next
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

    /// Records that the page was finished, once; not an undo step.
    func markCompleted(at date: Date = .now) {
        guard document.completedAt == nil else { return }
        document.completedAt = date
    }

    private func apply(_ action: ColoringAction) {
        switch action {
        case let .fill(regionId, color): document.fills[regionId] = color
        case let .stroke(stroke): document.strokes.append(stroke)
        case let .clearRegion(regionId): document.fills.removeValue(forKey: regionId)
        case .reset:
            document.fills.removeAll()
            document.strokes.removeAll()
            document.completedAt = nil
        case .undo, .redo: break
        }
    }
}
