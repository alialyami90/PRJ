import SwiftUI
import UIKit
import UIKit.UIGestureRecognizerSubclass

/// A number written on the page in Paint by Number mode.
struct PageNumber: Equatable {
    let regionId: UInt32
    let number: Int
    let label: RegionLabel
    let isSelected: Bool
}

/// The page itself: the rendered scene in a zoomable scroll view. Pinch to zoom; pan with one finger
/// in Fill and Paint by Number, with two in Freestyle, where one finger draws.
/// Every point handed back is in image pixels.
struct PageView: UIViewRepresentable {
    let image: CGImage
    var numbers: [PageNumber] = []
    var isDrawing = false
    var brushColor = "#000000"
    /// In image pixels.
    var brushWidth: Double = 24
    var onTap: (_ point: CGPoint, _ tolerance: Int) -> Void = { _, _ in }
    var onStroke: (_ points: [CGPoint]) -> Void = { _ in }

    func makeUIView(context: Context) -> PageScrollView { PageScrollView() }

    func updateUIView(_ view: PageScrollView, context: Context) {
        view.onTap = onTap
        view.onStroke = onStroke
        view.brushColor = UIColor(Color(hex: brushColor))
        view.brushWidth = brushWidth
        view.isDrawing = isDrawing
        view.setImage(image)
        view.setNumbers(numbers)
    }
}

final class PageScrollView: UIScrollView, UIScrollViewDelegate {
    var onTap: (CGPoint, Int) -> Void = { _, _ in }
    var onStroke: ([CGPoint]) -> Void = { _ in }
    var brushColor: UIColor = .black
    var brushWidth: Double = 24
    var isDrawing = false {
        didSet { if oldValue != isDrawing { updateGestures() } }
    }

    /// How far (in points on screen) a tap may miss a region and still count.
    private let touchSlop: CGFloat = 12
    private let page = UIView()
    private let imageView = UIImageView()
    private let numbersLayer = CALayer()
    private var numberLayers: [UInt32: CATextLayer] = [:]
    private var currentNumbers: [PageNumber] = []
    private var imageSize: CGSize = .zero
    private var fitted = false
    /// The stroke under the finger.
    private let liveStroke = CAShapeLayer()
    private var livePoints: [CGPoint] = []
    /// Strokes handed to the document but not yet in the rendered image; dropped when the next image arrives.
    private var pendingStrokes: [CAShapeLayer] = []
    private let gestureDelegate = SimultaneousGestures()
    private lazy var tap = UITapGestureRecognizer(target: self, action: #selector(handleTap(_:)))
    private lazy var draw = DrawGestureRecognizer(target: self, action: #selector(handleDraw(_:)))

    override init(frame: CGRect) {
        super.init(frame: frame)
        delegate = self
        backgroundColor = .clear
        showsHorizontalScrollIndicator = false
        showsVerticalScrollIndicator = false
        contentInsetAdjustmentBehavior = .never
        decelerationRate = .fast

        imageView.layer.cornerRadius = 16
        imageView.layer.masksToBounds = true
        imageView.layer.minificationFilter = .trilinear
        page.layer.shadowColor = UIColor.black.cgColor
        page.layer.shadowOpacity = 0.15
        page.layer.shadowRadius = 12
        page.layer.shadowOffset = CGSize(width: 0, height: 6)
        page.addSubview(imageView)
        style(liveStroke)
        page.layer.addSublayer(liveStroke)
        page.layer.addSublayer(numbersLayer)
        addSubview(page)

        tap.delegate = gestureDelegate
        draw.delegate = gestureDelegate
        addGestureRecognizer(tap)
        addGestureRecognizer(draw)
        updateGestures()
    }

    @available(*, unavailable)
    required init?(coder: NSCoder) { fatalError("init(coder:) is not used") }

    // MARK: Content

    func setImage(_ cgImage: CGImage) {
        guard imageView.image?.cgImage !== cgImage else { return }
        imageView.image = UIImage(cgImage: cgImage)
        CATransaction.begin()
        CATransaction.setDisableActions(true)
        pendingStrokes.forEach { $0.removeFromSuperlayer() }
        pendingStrokes.removeAll()
        CATransaction.commit()
        let size = CGSize(width: cgImage.width, height: cgImage.height)
        guard size != imageSize else { return }
        imageSize = size
        zoomScale = 1
        page.frame = CGRect(origin: .zero, size: size)
        imageView.frame = page.bounds
        page.layer.shadowPath = UIBezierPath(roundedRect: page.bounds, cornerRadius: 16).cgPath
        numbersLayer.frame = page.bounds
        liveStroke.frame = page.bounds
        contentSize = size
        fitted = false
        setNeedsLayout()
    }

    func setNumbers(_ numbers: [PageNumber]) {
        guard numbers != currentNumbers else { return }
        currentNumbers = numbers
        CATransaction.begin()
        CATransaction.setDisableActions(true)
        var keep = Set<UInt32>()
        for number in numbers {
            keep.insert(number.regionId)
            if let layer = numberLayers[number.regionId] {
                style(layer, for: number)
            } else {
                let layer = CATextLayer()
                layer.alignmentMode = .center
                numbersLayer.addSublayer(layer)
                numberLayers[number.regionId] = layer
                style(layer, for: number)
            }
        }
        for (id, layer) in numberLayers where !keep.contains(id) {
            layer.removeFromSuperlayer()
            numberLayers[id] = nil
        }
        CATransaction.commit()
    }

    private func style(_ layer: CATextLayer, for number: PageNumber) {
        // Bigger regions get bigger numbers, within what is readable once zoomed in.
        let size = CGFloat(min(max(number.label.radius * 1.1, 18), 72))
        layer.string = "\(number.number)"
        layer.font = UIFont.systemFont(ofSize: size, weight: number.isSelected ? .heavy : .semibold)
        layer.fontSize = size
        layer.foregroundColor = (number.isSelected ? UIColor.systemBlue : UIColor(white: 0.4, alpha: 1)).cgColor
        layer.contentsScale = textScale
        let width = size * 2.2, height = size * 1.25
        layer.frame = CGRect(x: number.label.point.x - width / 2, y: number.label.point.y - height / 2,
                             width: width, height: height)
    }

    /// Text is rasterised per layer: keep it sharp at the current zoom.
    private var textScale: CGFloat {
        let screen = traitCollection.displayScale > 0 ? traitCollection.displayScale : 2
        return min(screen * max(zoomScale, 0.25), 16)
    }

    private func updateTextScale() {
        CATransaction.begin()
        CATransaction.setDisableActions(true)
        let scale = textScale
        numberLayers.values.forEach { $0.contentsScale = scale }
        CATransaction.commit()
    }

    // MARK: Zoom

    override func layoutSubviews() {
        super.layoutSubviews()
        guard imageSize.width > 0, imageSize.height > 0, bounds.width > 0, bounds.height > 0 else { return }
        let fit = min(bounds.width / imageSize.width, bounds.height / imageSize.height)
        if !fitted || abs(fit - minimumZoomScale) > 0.0001 {
            let wasFitted = !fitted || zoomScale <= minimumZoomScale + 0.0001
            minimumZoomScale = fit
            maximumZoomScale = fit * 6
            if wasFitted { zoomScale = fit }
            fitted = true
            updateTextScale()
        }
        centerPage()
    }

    /// Letterbox the page in the middle while it is smaller than the view.
    private func centerPage() {
        let dx = max(0, (bounds.width - contentSize.width) / 2)
        let dy = max(0, (bounds.height - contentSize.height) / 2)
        let inset = UIEdgeInsets(top: dy, left: dx, bottom: dy, right: dx)
        if contentInset != inset { contentInset = inset }
    }

    func viewForZooming(in scrollView: UIScrollView) -> UIView? { page }
    func scrollViewDidZoom(_ scrollView: UIScrollView) { centerPage() }
    func scrollViewDidEndZooming(_ scrollView: UIScrollView, with view: UIView?, atScale scale: CGFloat) {
        updateTextScale()
    }

    // MARK: Touches

    private func updateGestures() {
        tap.isEnabled = !isDrawing
        draw.isEnabled = isDrawing
        panGestureRecognizer.minimumNumberOfTouches = isDrawing ? 2 : 1
    }

    @objc private func handleTap(_ gesture: UITapGestureRecognizer) {
        let point = gesture.location(in: page)
        guard page.bounds.contains(point) else { return }
        onTap(point, Int((touchSlop / max(zoomScale, 0.01)).rounded(.up)))
    }

    @objc private func handleDraw(_ gesture: DrawGestureRecognizer) {
        let point = gesture.location(in: page)
        switch gesture.state {
        case .began:
            livePoints = [point]
            updateLiveStroke()
        case .changed:
            livePoints.append(point)
            updateLiveStroke()
        case .ended:
            let points = livePoints
            livePoints = []
            // Keep showing the stroke until the re-rendered page (which includes it) arrives.
            let pending = CAShapeLayer()
            style(pending)
            pending.frame = page.bounds
            pending.path = liveStroke.path
            pending.strokeColor = liveStroke.strokeColor
            pending.lineWidth = liveStroke.lineWidth
            page.layer.insertSublayer(pending, below: liveStroke)
            pendingStrokes.append(pending)
            clearLiveStroke()
            onStroke(points)
        default:
            livePoints = []
            clearLiveStroke()
        }
    }

    private func style(_ layer: CAShapeLayer) {
        layer.fillColor = nil
        layer.lineCap = .round
        layer.lineJoin = .round
    }

    private func updateLiveStroke() {
        guard let first = livePoints.first else { return }
        let path = UIBezierPath()
        path.move(to: first)
        livePoints.dropFirst().forEach { path.addLine(to: $0) }
        if livePoints.count == 1 { path.addLine(to: first) } // a dot
        CATransaction.begin()
        CATransaction.setDisableActions(true)
        liveStroke.strokeColor = brushColor.cgColor
        liveStroke.lineWidth = CGFloat(brushWidth)
        liveStroke.path = path.cgPath
        CATransaction.commit()
    }

    private func clearLiveStroke() {
        CATransaction.begin()
        CATransaction.setDisableActions(true)
        liveStroke.path = nil
        CATransaction.commit()
    }
}

/// One-finger drawing that starts on touch down (no movement threshold, so dots work) and
/// gives way as soon as a second finger lands, letting the scroll view pinch and pan.
final class DrawGestureRecognizer: UIGestureRecognizer {
    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent) {
        super.touchesBegan(touches, with: event)
        if numberOfTouches > 1 || touches.count > 1 {
            state = state == .possible ? .failed : .cancelled
        } else if state == .possible {
            state = .began
        }
    }

    override func touchesMoved(_ touches: Set<UITouch>, with event: UIEvent) {
        super.touchesMoved(touches, with: event)
        if state == .began || state == .changed { state = .changed }
    }

    override func touchesEnded(_ touches: Set<UITouch>, with event: UIEvent) {
        super.touchesEnded(touches, with: event)
        state = (state == .began || state == .changed) ? .ended : .failed
    }

    override func touchesCancelled(_ touches: Set<UITouch>, with event: UIEvent) {
        super.touchesCancelled(touches, with: event)
        state = .cancelled
    }
}

/// Lets taps and drawing coexist with the scroll view's own pinch and pan.
private final class SimultaneousGestures: NSObject, UIGestureRecognizerDelegate {
    func gestureRecognizer(_ gestureRecognizer: UIGestureRecognizer,
                           shouldRecognizeSimultaneouslyWith other: UIGestureRecognizer) -> Bool {
        true
    }
}
