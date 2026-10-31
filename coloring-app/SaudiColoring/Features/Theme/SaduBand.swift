import SwiftUI

/// A strip of Al-Sadu, the Bedouin weaving on UNESCO's list for Saudi Arabia: a red ground, rows of
/// black teeth along both edges, and a chain of diamonds down the middle. Height sets the scale.
/// Drawn, not bitmapped, so it stays sharp at every size. Its colours are the weave's own and do not
/// change with dark mode.
struct SaduBand: View {
    var body: some View {
        Canvas { context, size in
            SaduPainter(size: size).paint(in: &context)
        }
        .accessibilityHidden(true)
    }
}

private struct SaduPainter {
    static let red = Color(hex: "#9E2B25")
    static let wool = Color(hex: "#F3EADF")
    static let black = Color(hex: "#1E1513")
    static let gold = Color(hex: "#D9A13A")

    let size: CGSize
    private var h: CGFloat { size.height }
    private var w: CGFloat { size.width }

    func paint(in c: inout GraphicsContext) {
        c.fill(Path(CGRect(origin: .zero, size: size)), with: .color(Self.red))

        // Cream selvedge lines along both edges.
        let edge = max(1.5, h * 0.09)
        c.fill(Path(CGRect(x: 0, y: 0, width: w, height: edge)), with: .color(Self.wool))
        c.fill(Path(CGRect(x: 0, y: h - edge, width: w, height: edge)), with: .color(Self.wool))

        // Black teeth pointing in from each edge.
        let tooth = h * 0.22
        repeatAcross(tooth) { x, _ in
            c.fill(polygon([CGPoint(x: x, y: edge), CGPoint(x: x + tooth, y: edge), CGPoint(x: x + tooth / 2, y: edge + tooth * 0.75)]),
                   with: .color(Self.black))
            c.fill(polygon([CGPoint(x: x, y: h - edge), CGPoint(x: x + tooth, y: h - edge), CGPoint(x: x + tooth / 2, y: h - edge - tooth * 0.75)]),
                   with: .color(Self.black))
        }

        // The diamond chain: cream and gold in turn, each with a black eye.
        let mid = h / 2, dh = h * 0.22, unit = dh * 2.5
        repeatAcross(unit) { x, i in
            let cx = x + unit / 2
            c.fill(diamond(cx, mid, dh * 1.15, dh), with: .color(i.isMultiple(of: 2) ? Self.wool : Self.gold))
            c.fill(diamond(cx, mid, dh * 0.42, dh * 0.38), with: .color(Self.black))
        }
    }

    private func repeatAcross(_ unit: CGFloat, _ draw: (CGFloat, Int) -> Void) {
        guard unit > 0 else { return }
        var x: CGFloat = 0, i = 0
        while x < w + unit {
            draw(x, i)
            x += unit
            i += 1
        }
    }

    private func diamond(_ cx: CGFloat, _ cy: CGFloat, _ dx: CGFloat, _ dy: CGFloat) -> Path {
        polygon([CGPoint(x: cx - dx, y: cy), CGPoint(x: cx, y: cy - dy), CGPoint(x: cx + dx, y: cy), CGPoint(x: cx, y: cy + dy)])
    }

    private func polygon(_ points: [CGPoint]) -> Path {
        var p = Path()
        p.addLines(points)
        p.closeSubpath()
        return p
    }
}

#Preview {
    VStack(spacing: 16) {
        SaduBand().frame(height: 12)
        SaduBand().frame(height: 30)
    }
    .padding()
}
