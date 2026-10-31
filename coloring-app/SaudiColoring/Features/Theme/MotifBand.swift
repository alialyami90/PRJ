import SwiftUI

/// A strip of a region's ornament, repeated across the available width. Height sets the scale.
/// Drawn, not bitmapped, so it stays sharp at every size and recolours with the theme.
struct MotifBand: View {
    enum Surface {
        /// On the region's ground colour (header bands): light shapes.
        case ground
        /// On the system background (the colour tray's top edge): shapes in the region's ground colour.
        case paper
    }

    let theme: RegionTheme
    var surface: Surface = .ground

    var body: some View {
        Canvas { context, size in
            let colors = palette
            context.fill(Path(CGRect(origin: .zero, size: size)), with: .color(colors.bg))
            MotifPainter(motif: theme.motif, size: size, fg: colors.fg, second: colors.second, bg: colors.bg)
                .paint(in: &context)
        }
        .accessibilityHidden(true)
    }

    private var palette: (bg: Color, fg: Color, second: Color) {
        switch surface {
        case .ground: (theme.ground, Color.white.opacity(0.94), theme.accent)
        case .paper: (Color(uiColor: .systemBackground), theme.ground, theme.accent)
        }
    }
}

/// The geometry of each ornament. One unit is sized from the band's height and repeated to the end.
private struct MotifPainter {
    let motif: RegionTheme.Motif
    let size: CGSize
    let fg: Color
    let second: Color
    let bg: Color

    private var h: CGFloat { size.height }
    private var w: CGFloat { size.width }

    func paint(in context: inout GraphicsContext) {
        switch motif {
        case .najdi: najdi(&context)
        case .rawashin: rawashin(&context)
        case .khoos: khoos(&context)
        case .qatt: qatt(&context)
        case .nabataean: nabataean(&context)
        case .arches: arches(&context)
        case .waves: waves(&context)
        case .sadu: sadu(&context)
        case .diamonds: diamonds(&context)
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

    private func polygon(_ points: [CGPoint]) -> Path {
        var p = Path()
        p.addLines(points)
        p.closeSubpath()
        return p
    }

    /// Triangle crenellations on a wall line, each with a small vent.
    private func najdi(_ c: inout GraphicsContext) {
        let line = h * 0.16, unit = h * 0.95, base = h * 0.78, top = h * 0.1
        c.fill(Path(CGRect(x: 0, y: h - line, width: w, height: line)), with: .color(fg))
        repeatAcross(unit) { x, _ in
            let cx = x + unit / 2
            c.fill(polygon([CGPoint(x: cx - base / 2, y: h - line), CGPoint(x: cx, y: top), CGPoint(x: cx + base / 2, y: h - line)]), with: .color(fg))
            let v = base * 0.26
            c.fill(polygon([CGPoint(x: cx - v / 2, y: h - line - h * 0.1), CGPoint(x: cx, y: h - line - h * 0.1 - v * 1.1),
                            CGPoint(x: cx + v / 2, y: h - line - h * 0.1)]), with: .color(second))
        }
    }

    /// Two rails and a diagonal wooden lattice between them.
    private func rawashin(_ c: inout GraphicsContext) {
        let rail = h * 0.14, spacing = h * 0.42, stroke = max(1.5, h * 0.07)
        var lattice = Path()
        var x = -h
        while x < w + h {
            lattice.move(to: CGPoint(x: x, y: rail))
            lattice.addLine(to: CGPoint(x: x + (h - 2 * rail), y: h - rail))
            lattice.move(to: CGPoint(x: x + (h - 2 * rail), y: rail))
            lattice.addLine(to: CGPoint(x: x, y: h - rail))
            x += spacing
        }
        c.stroke(lattice, with: .color(fg.opacity(0.85)), lineWidth: stroke)
        c.fill(Path(CGRect(x: 0, y: 0, width: w, height: rail)), with: .color(fg))
        c.fill(Path(CGRect(x: 0, y: h - rail, width: w, height: rail)), with: .color(fg))
        repeatAcross(spacing * 2) { x, _ in
            c.fill(Path(ellipseIn: CGRect(x: x - rail * 0.45, y: rail * 0.05, width: rail * 0.9, height: rail * 0.9)), with: .color(second))
        }
    }

    /// Plaited palm strips: chevrons in two alternating colours.
    private func khoos(_ c: inout GraphicsContext) {
        let unit = h * 0.62, thick = unit * 0.55
        repeatAcross(unit) { x, i in
            let shape = polygon([
                CGPoint(x: x, y: 0), CGPoint(x: x + thick, y: 0), CGPoint(x: x + thick + h / 2 * 0.6, y: h / 2),
                CGPoint(x: x + thick, y: h), CGPoint(x: x, y: h), CGPoint(x: x + h / 2 * 0.6, y: h / 2),
            ])
            c.fill(shape, with: .color(i.isMultiple(of: 2) ? fg : second))
        }
    }

    /// Al-Qatt: a row of painted stripes over a row of triangles.
    private func qatt(_ c: inout GraphicsContext) {
        let stripes: [Color] = [fg, second, Color(hex: "#3F8F3A"), Color(hex: "#2B5BA8"), Color(hex: "#1E1513")]
        let stripeH = h * 0.5, stripe = h * 0.2
        repeatAcross(stripe) { x, i in
            c.fill(Path(CGRect(x: x, y: 0, width: stripe, height: stripeH)), with: .color(stripes[i % stripes.count]))
        }
        c.fill(Path(CGRect(x: 0, y: stripeH, width: w, height: h * 0.06)), with: .color(fg))
        let unit = h * 0.5, top = stripeH + h * 0.06
        repeatAcross(unit) { x, i in
            c.fill(polygon([CGPoint(x: x, y: h), CGPoint(x: x + unit / 2, y: top), CGPoint(x: x + unit, y: h)]),
                   with: .color(i.isMultiple(of: 2) ? second : fg))
        }
    }

    /// Hegra's crow-step crowns: three steps up, three steps down.
    private func nabataean(_ c: inout GraphicsContext) {
        let unit = h * 1.5, step = h * 0.24, base = unit * 0.82, line = h * 0.12
        c.fill(Path(CGRect(x: 0, y: h - line, width: w, height: line)), with: .color(second))
        repeatAcross(unit) { x, _ in
            let cx = x + unit / 2
            for level in 0..<3 {
                let width = base * (1 - CGFloat(level) * 0.3)
                c.fill(Path(CGRect(x: cx - width / 2, y: h - line - step * CGFloat(level + 1), width: width, height: step + 0.5)),
                       with: .color(fg))
            }
        }
    }

    /// An arcade: a solid band with round-topped openings.
    private func arches(_ c: inout GraphicsContext) {
        let unit = h * 0.95, opening = unit * 0.58, springLine = h * 0.52
        c.fill(Path(CGRect(x: 0, y: 0, width: w, height: h)), with: .color(fg))
        c.fill(Path(CGRect(x: 0, y: 0, width: w, height: h * 0.1)), with: .color(second))
        repeatAcross(unit) { x, _ in
            let cx = x + unit / 2, r = opening / 2
            var p = Path()
            p.move(to: CGPoint(x: cx - r, y: h))
            p.addLine(to: CGPoint(x: cx - r, y: springLine))
            p.addArc(center: CGPoint(x: cx, y: springLine), radius: r, startAngle: .degrees(180), endAngle: .degrees(0), clockwise: false)
            p.addLine(to: CGPoint(x: cx + r, y: h))
            p.closeSubpath()
            c.fill(p, with: .color(bg))
        }
    }

    /// Fish-scale waves: half circles rising from the bottom edge, a second colour inside each.
    private func waves(_ c: inout GraphicsContext) {
        let r = h * 0.62
        repeatAcross(r * 1.6) { x, _ in
            let cx = x + r * 0.8
            c.fill(Path(ellipseIn: CGRect(x: cx - r, y: h - r, width: 2 * r, height: 2 * r)), with: .color(fg))
            let inner = r * 0.55
            c.fill(Path(ellipseIn: CGRect(x: cx - inner, y: h - inner, width: 2 * inner, height: 2 * inner)), with: .color(second))
        }
    }

    /// Al-Sadu: rows of teeth above and below a chain of diamonds.
    private func sadu(_ c: inout GraphicsContext) {
        let black = Color(hex: "#1E1513")
        let edge = h * 0.1, tooth = h * 0.2
        c.fill(Path(CGRect(x: 0, y: 0, width: w, height: edge)), with: .color(fg))
        c.fill(Path(CGRect(x: 0, y: h - edge, width: w, height: edge)), with: .color(fg))
        repeatAcross(tooth) { x, _ in
            c.fill(polygon([CGPoint(x: x, y: edge), CGPoint(x: x + tooth, y: edge), CGPoint(x: x + tooth / 2, y: edge + tooth * 0.8)]), with: .color(black))
            c.fill(polygon([CGPoint(x: x, y: h - edge), CGPoint(x: x + tooth, y: h - edge), CGPoint(x: x + tooth / 2, y: h - edge - tooth * 0.8)]), with: .color(black))
        }
        let mid = h / 2, dh = h * 0.24, unit = dh * 2.4
        repeatAcross(unit) { x, i in
            let cx = x + unit / 2
            c.fill(polygon([CGPoint(x: cx - dh * 1.1, y: mid), CGPoint(x: cx, y: mid - dh), CGPoint(x: cx + dh * 1.1, y: mid), CGPoint(x: cx, y: mid + dh)]),
                   with: .color(i.isMultiple(of: 2) ? fg : second))
            let s = dh * 0.4
            c.fill(polygon([CGPoint(x: cx - s, y: mid), CGPoint(x: cx, y: mid - s), CGPoint(x: cx + s, y: mid), CGPoint(x: cx, y: mid + s)]), with: .color(black))
        }
    }

    /// Najrani basket weave: a row of diamonds, alternating colours, each with an open centre.
    private func diamonds(_ c: inout GraphicsContext) {
        let unit = h * 0.8, line = h * 0.08
        c.fill(Path(CGRect(x: 0, y: 0, width: w, height: line)), with: .color(fg))
        c.fill(Path(CGRect(x: 0, y: h - line, width: w, height: line)), with: .color(fg))
        repeatAcross(unit) { x, i in
            let cx = x + unit / 2, mid = h / 2, dy = (h - 2 * line) / 2 * 0.92, dx = unit / 2
            c.fill(polygon([CGPoint(x: cx - dx, y: mid), CGPoint(x: cx, y: mid - dy), CGPoint(x: cx + dx, y: mid), CGPoint(x: cx, y: mid + dy)]),
                   with: .color(i.isMultiple(of: 2) ? fg : second))
            let s = 0.36
            c.fill(polygon([CGPoint(x: cx - dx * s, y: mid), CGPoint(x: cx, y: mid - dy * s), CGPoint(x: cx + dx * s, y: mid), CGPoint(x: cx, y: mid + dy * s)]),
                   with: .color(bg))
        }
    }
}

#Preview {
    let ids = ["riyadh", "jeddah", "al-ahsa", "asir", "alula", "tabuk", "jazan", "hail", "najran"]
    return VStack(spacing: 12) {
        ForEach(ids, id: \.self) { id in
            MotifBand(theme: .of(id)).frame(height: 28)
        }
    }
    .padding()
}
