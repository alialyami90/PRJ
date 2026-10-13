import SwiftUI

/// The scene, rendered from the document, filling the available space aspect-fit.
/// Taps are converted to image space and handed to `onTap` with a tolerance in image pixels,
/// so a tap that lands on an outline still finds the region a child was aiming at.
struct FillCanvas: View {
    let image: CGImage
    let onTap: (_ point: CGPoint, _ tolerance: Int) -> Void

    /// How far (in points on screen) a tap may miss a region and still count.
    private let touchSlop: CGFloat = 12

    var body: some View {
        GeometryReader { proxy in
            let geometry = CanvasGeometry(
                imageSize: CGSize(width: image.width, height: image.height),
                viewSize: proxy.size
            )
            Image(decorative: image, scale: 1)
                .resizable()
                .interpolation(.medium)
                .frame(width: geometry.imageFrame.width, height: geometry.imageFrame.height)
                .clipShape(RoundedRectangle(cornerRadius: 12))
                .shadow(color: .black.opacity(0.15), radius: 8, y: 4)
                .position(x: geometry.imageFrame.midX, y: geometry.imageFrame.midY)
                .contentShape(Rectangle())
                .gesture(SpatialTapGesture(coordinateSpace: .local).onEnded { value in
                    guard let point = geometry.imagePoint(fromView: value.location) else { return }
                    onTap(point, Int((touchSlop / geometry.scale).rounded(.up)))
                })
        }
    }
}
