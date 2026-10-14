import SwiftUI

/// A sum a grown-up can do and a 4 to 9 year old most likely cannot (App Review guideline 1.3).
/// Required before anything that leaves the app or plays an ad on request.
struct ParentalGateQuestion: Equatable {
    let a: Int
    let b: Int
    /// Four distinct positive answers, one of them right, in random order.
    let choices: [Int]

    var answer: Int { a * b }

    static func random<G: RandomNumberGenerator>(using rng: inout G) -> ParentalGateQuestion {
        let a = Int.random(in: 4...9, using: &rng), b = Int.random(in: 4...9, using: &rng)
        var choices: Set<Int> = [a * b]
        while choices.count < 4 {
            let wrong = a * b + Int.random(in: -15...15, using: &rng)
            if wrong > 0 { choices.insert(wrong) }
        }
        return ParentalGateQuestion(a: a, b: b, choices: Array(choices).shuffled(using: &rng))
    }

    static func random() -> ParentalGateQuestion {
        var rng = SystemRandomNumberGenerator()
        return random(using: &rng)
    }
}

/// "Ask a grown-up" sheet. Calls `onPass` after a right answer; a wrong one asks a new sum.
struct ParentalGate: View {
    let onPass: () -> Void
    @Environment(\.dismiss) private var dismiss
    @State private var question = ParentalGateQuestion.random()
    @State private var wrongAnswers = 0

    init(onPass: @escaping () -> Void) {
        self.onPass = onPass
    }

    var body: some View {
        VStack(spacing: 24) {
            Image(systemName: "person.2.fill")
                .font(.system(size: 56))
                .foregroundStyle(.tint)
            Text("Ask a grown-up")
                .font(.largeTitle.bold())
            Text("Grown-ups: what is \(question.a) × \(question.b)?")
                .font(.title2)
            HStack(spacing: 16) {
                ForEach(question.choices, id: \.self) { choice in
                    Button {
                        answer(choice)
                    } label: {
                        Text("\(choice)")
                            .font(.title.bold())
                            .frame(minWidth: 72, minHeight: 64)
                    }
                    .buttonStyle(.bordered)
                }
            }
            .modifier(Shake(amount: CGFloat(wrongAnswers)))
            .animation(.default, value: wrongAnswers)
            Button("Not now", systemImage: "xmark") { dismiss() }
                .font(.title3)
                .padding(.top, 8)
        }
        .padding(40)
        .presentationDetents([.medium])
    }

    private func answer(_ choice: Int) {
        if choice == question.answer {
            dismiss()
            onPass()
        } else {
            wrongAnswers += 1
            question = .random()
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
