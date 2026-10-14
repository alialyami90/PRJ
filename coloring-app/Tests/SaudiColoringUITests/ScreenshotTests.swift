import XCTest

/// Walks the main screens of a debug build started with demo progress (`-demoContent`, see
/// App/DemoContent.swift) and saves a screenshot of each: as test attachments, and as PNG files
/// in $SCREENSHOTS_DIR when it is set (pass it as TEST_RUNNER_SCREENSHOTS_DIR to xcodebuild).
/// Run with the Screenshots scheme; CI does it in .github/workflows/screenshots.yml.
final class ScreenshotTests: XCTestCase {
    private enum Titles {
        static let ukhdood = "Young explorers at Al-Ukhdood archaeological site"
        static let dam = "Family outing at the Najran dam overlook"
    }

    override func setUp() {
        continueAfterFailure = false
        XCUIDevice.shared.orientation = .landscapeLeft
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
        app.buttons["Numbers"].tap()
        pause(5) // where each number goes is worked out the first time Numbers opens
        snapshot("05-numbers")
    }

    func testFinishedPage() {
        let app = launch()
        open(Titles.dam, region: "Najran", in: app)
        XCTAssertTrue(app.staticTexts["You did it!"].waitForExistence(timeout: 20))
        pause(1.5) // the stars spring in
        snapshot("06-finished")
        app.buttons["Get more colours"].tap()
        XCTAssertTrue(app.staticTexts["Ask a grown-up"].waitForExistence(timeout: 10))
        pause(1)
        snapshot("07-parental-gate")
    }

    // MARK: Helpers

    private func launch() -> XCUIApplication {
        let app = XCUIApplication()
        app.launchArguments = ["-demoContent"]
        app.launch()
        XCUIDevice.shared.orientation = .landscapeLeft
        XCTAssertTrue(app.staticTexts["Najran"].waitForExistence(timeout: 60))
        pause(2) // gallery thumbnails
        return app
    }

    private func showRegion(_ name: String, in app: XCUIApplication) {
        app.staticTexts[name].firstMatch.tap()
        pause(2)
    }

    /// Opens a page from its region's gallery and waits for it to be drawn.
    private func open(_ title: String, region: String, in app: XCUIApplication) {
        showRegion(region, in: app)
        let card = app.staticTexts[title].firstMatch
        for _ in 0..<6 where !(card.exists && card.isHittable) {
            app.scrollViews.firstMatch.swipeUp()
        }
        card.tap()
        XCTAssertTrue(app.buttons["Numbers"].waitForExistence(timeout: 20))
        pause(3)
    }

    private func pause(_ seconds: TimeInterval) {
        Thread.sleep(forTimeInterval: seconds)
    }

    private func snapshot(_ name: String) {
        let screenshot = XCUIScreen.main.screenshot()
        let attachment = XCTAttachment(screenshot: screenshot)
        attachment.name = name
        attachment.lifetime = .keepAlways
        add(attachment)
        guard let dir = ProcessInfo.processInfo.environment["SCREENSHOTS_DIR"], !dir.isEmpty else { return }
        let folder = URL(fileURLWithPath: dir, isDirectory: true)
        try? FileManager.default.createDirectory(at: folder, withIntermediateDirectories: true)
        try? screenshot.pngRepresentation.write(to: folder.appendingPathComponent("\(name).png"))
    }
}
