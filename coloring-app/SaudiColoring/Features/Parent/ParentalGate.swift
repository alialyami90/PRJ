import SwiftUI

/// A sum a grown-up can do and a 4 to 9 year old cannot (App Review guideline 1.3): a two-digit number
/// times a one-digit one, answered by typing the digits. With no choices to guess from, mashing almost
/// never gets through, and three wrong answers close the gate.
/// Required before anything that leaves the app or plays an ad on request.
struct ParentalGateQuestion: Equatable {
    let a: Int
    let b: Int

    var answer: Int { a * b }

    /// The gate closes after this many wrong answers.
    static let maxWrongAnswers = 3
    /// The longest answer is 19 × 9 = 171.
    static let maxDigits = 3

    func isRight(_ typed: String) -> Bool { Int(typed) == answer }

    static func random<G: RandomNumberGenerator>(using rng: inout G) -> ParentalGateQuestion {
        ParentalGateQuestion(a: Int.random(in: 12...19, using: &rng), b: Int.random(in: 3...9, using: &rng))
    }

    static func random() -> ParentalGateQuestion {
        var rng = SystemRandomNumberGenerator()
        return random(using: &rng)
    }
}

/// "Ask a grown-up" sheet. Calls `onPass` after a right answer; a wrong one asks a new sum, and the
/// third wrong one closes the sheet. Deliberately the stock system look: grown-up territory.
struct ParentalGate: View {
    let onPass: () -> Void
    @Environment(\.dismiss) private var dismiss
    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    @State private var question = ParentalGateQuestion.random()
    @State private var typed = ""
    @State private var wrongAnswers = 0

    init(onPass: @escaping () -> Void) {
        self.onPass = onPass
    }

    var body: some View {
        VStack(spacing: 20) {
            Image(systemName: "person.2.fill")
                .font(.largeTitle)
                .imageScale(.large)
                .foregroundStyle(.tint)
                .accessibilityHidden(true)
            Text("Ask a grown-up")
                .font(.largeTitle.bold())
            Text("Grown-ups: what is \(question.a) × \(question.b)?")
                .font(.title2)
                .multilineTextAlignment(.center)
            Text(typed.isEmpty ? " " : typed)
                .font(.largeTitle.monospacedDigit().bold())
                .frame(maxWidth: 220, minHeight: 64)
                .background(.quaternary, in: RoundedRectangle(cornerRadius: 14, style: .continuous))
                .modifier(Shake(amount: CGFloat(wrongAnswers)))
                .animation(reduceMotion ? nil : .default, value: wrongAnswers)
                .accessibilityLabel(Text("Answer"))
                .accessibilityValue(Text(typed))
            keypad
            Button("Not now", systemImage: "xmark") { dismiss() }
                .font(.title3)
                .frame(minHeight: 44)
        }
        .padding(.horizontal, 24)
        .padding(.vertical, 28)
        .frame(maxWidth: 560)
        .presentationDetents([.large])
        // The digits read left to right in every language.
        .environment(\.layoutDirection, .leftToRight)
    }

    /// 1 to 9, then delete, 0 and OK.
    private var keypad: some View {
        Grid(horizontalSpacing: 12, verticalSpacing: 12) {
            ForEach(0..<3) { row in
                GridRow {
                    ForEach(1...3, id: \.self) { column in digit(row * 3 + column) }
                }
            }
            GridRow {
                key {
                    Image(systemName: "delete.left")
                } action: {
                    if !typed.isEmpty { typed.removeLast() }
                }
                .accessibilityLabel(Text("Delete"))
                digit(0)
                Button(action: check) {
                    Text("OK")
                        .font(.title.bold())
                        .frame(maxWidth: .infinity, minHeight: 56)
                }
                .buttonStyle(.borderedProminent)
                .disabled(typed.isEmpty)
            }
        }
        .frame(maxWidth: 360)
    }

    private func digit(_ n: Int) -> some View {
        key {
            Text("\(n)")
        } action: {
            if typed.count < ParentalGateQuestion.maxDigits { typed.append(String(n)) }
        }
    }

    private func key<Label: View>(@ViewBuilder _ label: () -> Label, action: @escaping () -> Void) -> some View {
        Button(action: action) {
            label()
                .font(.title.bold())
                .frame(maxWidth: .infinity, minHeight: 56)
        }
        .buttonStyle(.bordered)
    }

    private func check() {
        if question.isRight(typed) {
            dismiss()
            onPass()
        } else {
            wrongAnswers += 1
            typed = ""
            if wrongAnswers >= ParentalGateQuestion.maxWrongAnswers {
                dismiss()
            } else {
                question = .random()
            }
        }
    }
}

/// Side-to-side wobble; animate `amount` by whole numbers.
private struct Shake: GeometryEffect {
    var amount: CGFloat
    var animatableData: CGFloat {
        get { amount }
        set { amount = newValue }
    }

    func effectValue(size: CGSize) -> ProjectionTransform {
        ProjectionTransform(CGAffineTransform(translationX: 10 * sin(amount * .pi * 4), y: 0))
    }
}

#Preview {
    ParentalGate {}
}
