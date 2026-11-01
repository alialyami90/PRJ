import UIKit
import XCTest

/// Walks the main screens of a debug build started with demo progress (`-demoContent`, see
/// App/DemoContent.swift) and saves a screenshot of each: as test attachments, and as PNG files
/// in $SCREENSHOTS_DIR when it is set (pass it as TEST_RUNNER_SCREENSHOTS_DIR to xcodebuild).
/// Run with the Screenshots scheme; CI does it in .github/workflows/screenshots.yml.
final class ScreenshotTests: XCTestCase {
    private enum Titles {
        static let ukhdood = "Al-Ukhdood Explorers"
        static let dam = "Najran Dam"
    }

    /// iPad in landscape, iPhone in portrait: how each is mostly held.
    private var isPhone: Bool { UIDevice.current.userInterfaceIdiom == .phone }
    private var orientation: UIDeviceOrientation { isPhone ? .portrait : .landscapeLeft }

    override func setUp() {
        continueAfterFailure = false
        XCUIDevice.shared.orientation = orientation
    }

    func testHomeAndGallery() {
        let app = launch()
        snapshot("01-home")
        showRegion("Najran", in: app)
        XCTAssertTrue(app.staticTexts[Titles.ukhdood].waitForExistence(timeout: 10))
        snapshot("02-gallery")
    }

    func testModes() {
        let app = launch()
        open(Titles.ukhdood, region: "Najran", in: app)
        snapshot("03-fill")
        app.buttons["Paint"].tap()
        pause(1)
        snapshot("04-paint")
    }

    func testFinishedPage() {
        let app = launch()
        open(Titles.dam, region: "Najran", in: app)
        XCTAssertTrue(app.staticTexts["You did it!"].waitForExistence(timeout: 20))
        pause(1.5) // the seal presses down
        snapshot("06-finished")
        app.buttons["Keep coloring"].tap()
        // The bonus colours sit behind the grown-up lock at the end of the colour tray.
        // It starts off screen, where asking whether it is hittable fails the test, so swipe the tray
        // until its frame is inside the window.
        let lock = app.buttons["More colors"].firstMatch
        XCTAssertTrue(lock.waitForExistence(timeout: 10))
        let tray = app.scrollViews.containing(NSPredicate(format: "label == %@", "More colors")).firstMatch
        let window = app.windows.firstMatch
        for _ in 0..<8 where !window.frame.contains(lock.frame) {
            tray.swipeLeft()
        }
        lock.tap()
        XCTAssertTrue(app.staticTexts["Ask a grown-up"].waitForExistence(timeout: 10))
        pause(1)
        snapshot("07-parental-gate")
    }

    // MARK: Helpers

    private func launch() -> XCUIApplication {
        let app = XCUIApplication()
        app.launchArguments = ["-demoContent"]
        app.launch()
        XCUIDevice.shared.orientation = orientation
        XCTAssertTrue(app.buttons["Najran"].waitForExistence(timeout: 60))
        pause(2) // gallery thumbnails
        return app
    }

    /// Taps the region's stop on the journey rail.
    private func showRegion(_ name: String, in app: XCUIApplication) {
        app.buttons[name].firstMatch.tap()
        pause(2)
    }

    /// Opens a page from its region's gallery and waits for it to be drawn.
    private func open(_ title: String, region: String, in app: XCUIApplication) {
        showRegion(region, in: app)
        let card = app.staticTexts[title].firstMatch
        // Drag on the trailing side of the window, where the gallery is on iPad and the whole screen is on iPhone.
        let window = app.windows.firstMatch
        for _ in 0..<8 where !(card.exists && card.isHittable) {
            window.coordinate(withNormalizedOffset: CGVector(dx: 0.75, dy: 0.75))
                .press(forDuration: 0.05, thenDragTo: window.coordinate(withNormalizedOffset: CGVector(dx: 0.75, dy: 0.35)))
        }
        card.tap()
        XCTAssertTrue(app.buttons["Paint"].waitForExistence(timeout: 20))
        pause(3)
    }

    private func pause(_ seconds: TimeInterval) {
        Thread.sleep(forTimeInterval: seconds)
    }

    private func snapshot(_ name: String) {
        let file = isPhone ? "phone-\(name)" : name
        let screenshot = XCUIScreen.main.screenshot()
        let attachment = XCTAttachment(screenshot: screenshot)
        attachment.name = file
        attachment.lifetime = .keepAlways
        add(attachment)
        guard let dir = ProcessInfo.processInfo.environment["SCREENSHOTS_DIR"], !dir.isEmpty else { return }
        let folder = URL(fileURLWithPath: dir, isDirectory: true)
        try? FileManager.default.createDirectory(at: folder, withIntermediateDirectories: true)
        try? screenshot.pngRepresentation.write(to: folder.appendingPathComponent("\(file).png"))
    }
}
