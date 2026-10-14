import CoreGraphics

/// Maps between the on-screen canvas and image space when the scene is drawn aspect-fit and centred.
struct CanvasGeometry {
    let imageSize: CGSize
    let viewSize: CGSize

    var scale: CGFloat {
        guard imageSize.width > 0, imageSize.height > 0 else { return 0 }
        return min(viewSize.width / imageSize.width, viewSize.height / imageSize.height)
    }

    /// Where the image sits inside the view.
    var imageFrame: CGRect {
        let size = CGSize(width: imageSize.width * scale, height: imageSize.height * scale)
        return CGRect(
            x: (viewSize.width - size.width) / 2,
            y: (viewSize.height - size.height) / 2,
            width: size.width, height: size.height
        )
    }

    /// Image-space point for a view-space touch, or nil when the touch is in the letterbox.
    func imagePoint(fromView point: CGPoint) -> CGPoint? {
        let frame = imageFrame
        guard scale > 0, frame.contains(point) else { return nil }
        return CGPoint(x: (point.x - frame.minX) / scale, y: (point.y - frame.minY) / scale)
    }
}
