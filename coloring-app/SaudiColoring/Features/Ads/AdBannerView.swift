import SwiftUI
import UIKit

/// The gallery's banner slot. Never placed over the canvas.
struct AdBannerView: UIViewRepresentable {
    let ads: AdService

    func makeUIView(context: Context) -> UIView {
        let container = UIView()
        if let banner = ads.makeBannerView() {
            banner.translatesAutoresizingMaskIntoConstraints = false
            container.addSubview(banner)
            NSLayoutConstraint.activate([
                banner.centerXAnchor.constraint(equalTo: container.centerXAnchor),
                banner.centerYAnchor.constraint(equalTo: container.centerYAnchor),
            ])
        }
        return container
    }

    func updateUIView(_ uiView: UIView, context: Context) {}
}
