#if DEBUG
import CoreGraphics
import Foundation

/// Debug builds only: launching with `-demoContent` starts from a few pages already coloured,
/// kept in memory, so the screenshot run (Tests/SaudiColoringUITests) shows the app in use.
enum DemoContent {
    static let launchArgument = "-demoContent"

    static var isRequested: Bool { ProcessInfo.processInfo.arguments.contains(launchArgument) }

    private struct Page {
        let regionId: String
        let sceneId: String
        /// Shapes left of this fraction of the page's width are coloured, as if the child worked left to right.
        let progress: Double
        /// Shows the gallery's "finished" star. A full page without it opens on "You did it!".
        var completed = false
        /// A rainbow drawn with the brush.
        var rainbow = false
    }

    private static let pages: [Page] = [
        Page(regionId: "riyadh", sceneId: "masmak-fort", progress: 1, completed: true),
        Page(regionId: "riyadh", sceneId: "kingdom-tower-skyline", progress: 0.6),
        Page(regionId: "riyadh", sceneId: "ardah-dance", progress: 0.35),
        Page(regionId: "najran", sceneId: "al-aan-palace", progress: 1, completed: true),
        Page(regionId: "najran", sceneId: "al-ukhdood", progress: 0.55, rainbow: true),
        Page(regionId: "najran", sceneId: "hima-rock-art", progress: 0.4),
        Page(regionId: "najran", sceneId: "najran-dam", progress: 1),
    ]

    static func environment() -> AppEnvironment {
        let defaults = UserDefaults(suiteName: "demo") ?? .standard
        defaults.removePersistentDomain(forName: "demo")
        // Decoding and rendering a page takes a moment; do the pages side by side.
        var seeded = [(ColoringDocument, Data?)?](repeating: nil, count: pages.count)
        let lock = NSLock()
        DispatchQueue.concurrentPerform(iterations: pages.count) { i in
            let result = seed(pages[i])
            lock.lock()
            seeded[i] = result
            lock.unlock()
        }
        let persistence = InMemoryPersistenceService()
        for case let (document, thumbnail)? in seeded {
            try? persistence.save(document)
            if let thumbnail {
                try? persistence.saveThumbnail(thumbnail, regionId: document.regionId, sceneId: document.sceneId)
            }
        }
        return AppEnvironment(catalog: SceneCatalog.loadFromBundle(), ads: NoOpAdService(),
                              persistence: persistence, rewards: RewardStore(defaults: defaults))
    }

    /// The page's progress and its gallery thumbnail.
    private static func seed(_ page: Page) -> (ColoringDocument, Data?)? {
        guard let assets = try? SceneAssets.load(regionId: page.regionId, sceneId: page.sceneId) else { return nil }
        let map = assets.map
        let limit = page.progress * Double(map.width)
        var fills: [UInt32: String] = [:]
        for (id, x) in centreX(of: map) where page.progress >= 1 || x < limit {
            fills[id] = assets.palette.entry(for: id)?.color ?? "#F4A62A"
        }
        let document = ColoringDocument(
            regionId: page.regionId, sceneId: page.sceneId, mode: .fill, fills: fills,
            strokes: page.rainbow ? rainbow(width: map.width, height: map.height) : [],
            updatedAt: Date(timeIntervalSinceNow: -3600),
            completedAt: page.completed ? Date(timeIntervalSinceNow: -3600) : nil
        )
        let thumbnail = CanvasRenderer(map: map).render(document).flatMap { CanvasRenderer.thumbnailPNG(of: $0) }
        return (document, thumbnail)
    }

    /// Mean x of every region, from every fourth pixel each way (plenty for ordering left to right).
    private static func centreX(of map: RegionMap) -> [UInt32: Double] {
        var sum: [UInt32: (x: Int, n: Int)] = [:]
        for id in map.regionIds { sum[id] = (0, 0) }
        for y in stride(from: 0, to: map.height, by: 4) {
            for x in stride(from: 0, to: map.width, by: 4) {
                let id = map.pixels[y * map.width + x]
                guard id != RegionMap.outline, let s = sum[id] else { continue }
                sum[id] = (s.x + x, s.n + 1)
            }
        }
        // Shapes too small to be sampled count as being on the right.
        return sum.mapValues { $0.n > 0 ? Double($0.x) / Double($0.n) : Double(map.width) }
    }

    /// Six arcs in the top right corner.
    private static func rainbow(width: Int, height: Int) -> [Stroke] {
        let colors = ["#E53935", "#FB8C00", "#FDD835", "#43A047", "#1E88E5", "#8E24AA"]
        let cx = Double(width) * 0.8, cy = Double(height) * 0.32, band = 26.0
        return colors.enumerated().map { i, color in
            let r = 230 - Double(i) * band
            let points = stride(from: 0.0, through: Double.pi, by: Double.pi / 40).map {
                Stroke.Point(x: cx + r * cos($0), y: cy - r * sin($0))
            }
            return Stroke(color: color, width: band + 2, points: points)
        }
    }
}
#endif
