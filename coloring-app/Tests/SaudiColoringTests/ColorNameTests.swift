import XCTest
@testable import SaudiColoring

final class ColorNameTests: XCTestCase {
    func testTheCrayonBoxHasPlainNames() {
        let expected: [String: ColorName] = [
            "#E53935": .init(hue: .red), "#FB8C00": .init(hue: .orange), "#FDD835": .init(hue: .yellow),
            "#43A047": .init(hue: .green), "#00897B": .init(hue: .teal, shade: .dark), "#1E88E5": .init(hue: .blue),
            "#8E24AA": .init(hue: .purple), "#D81B60": .init(hue: .pink), "#6D4C41": .init(hue: .brown),
            "#9E9E9E": .init(hue: .gray), "#212121": .init(hue: .black), "#FFFFFF": .init(hue: .white),
        ]
        for (hex, name) in expected {
            XCTAssertEqual(ColorName(hex: hex), name, hex)
        }
    }

    func testPaleColoursAreLight() {
        XCTAssertEqual(ColorName(hex: "#82B1FF"), .init(hue: .blue, shade: .light))
        XCTAssertEqual(ColorName(hex: "#FF8A80"), .init(hue: .red, shade: .light))
        XCTAssertEqual(ColorName(hex: "#B0BEC5"), .init(hue: .gray, shade: .light))
    }

    func testEveryCrayonHasASpokenNameAndNoHexCode() {
        for hex in ColorTray.crayons + ColorTray.bonusColors {
            let spoken = ColorName(hex: hex).spoken
            XCTAssertFalse(spoken.isEmpty, hex)
            XCTAssertFalse(spoken.contains("#"), hex)
        }
    }
}
