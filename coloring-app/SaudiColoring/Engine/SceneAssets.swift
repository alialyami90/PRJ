import CoreGraphics
import Foundation
import ImageIO

/// The runtime half of the scene asset contract: the region map and the palette for one scene.
struct SceneAssets {
    let map: RegionMap
    let palette: Palette
    /// True when the scene's own art is not in the bundle yet and the built-in sample scene was used.
    let isSample: Bool

    enum LoadError: Error {
        case missing(String)
        case unreadableImage
    }

    /// Loads Scenes/<region>/<scene>/ (written by Scripts/sync_scenes.py), falling back to
    /// SampleScene/ so every scene is playable before its art is approved.
    static func load(regionId: String, sceneId: String, bundle: Bundle = .main) throws -> SceneAssets {
        if let assets = try load(directory: "Scenes/\(regionId)/\(sceneId)", bundle: bundle, isSample: false) {
            return assets
        }
        if let assets = try load(directory: "SampleScene", bundle: bundle, isSample: true) {
            return assets
        }
        throw LoadError.missing("\(regionId)/\(sceneId)")
    }

    private static func load(directory: String, bundle: Bundle, isSample: Bool) throws -> SceneAssets? {
        guard let mapURL = bundle.url(forResource: "regions", withExtension: "png", subdirectory: directory),
              let paletteURL = bundle.url(forResource: "palette", withExtension: "json", subdirectory: directory)
        else { return nil }
        guard let source = CGImageSourceCreateWithURL(mapURL as CFURL, nil),
              let image = CGImageSourceCreateImageAtIndex(source, 0, nil),
              let map = RegionMap(cgImage: image)
        else { throw LoadError.unreadableImage }
        let palette = try Palette.decode(from: Data(contentsOf: paletteURL))
        return SceneAssets(map: map, palette: palette, isSample: isSample)
    }
}
