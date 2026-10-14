import UIKit

/// Gallery art shipped by Scripts/sync_scenes.py under Scenes/ in the bundle.
enum BundleImages {
    /// The region's colour cover, Scenes/<region>/cover.png.
    static func cover(regionId: String, bundle: Bundle = .main) -> UIImage? {
        image("cover", in: "Scenes/\(regionId)", bundle: bundle)
    }

    /// The page's line art thumbnail, Scenes/<region>/<scene>/thumb.png.
    static func thumbnail(regionId: String, sceneId: String, bundle: Bundle = .main) -> UIImage? {
        image("thumb", in: "Scenes/\(regionId)/\(sceneId)", bundle: bundle)
    }

    private static func image(_ name: String, in directory: String, bundle: Bundle) -> UIImage? {
        guard let path = bundle.path(forResource: name, ofType: "png", inDirectory: directory) else { return nil }
        return UIImage(contentsOfFile: path)
    }
}
