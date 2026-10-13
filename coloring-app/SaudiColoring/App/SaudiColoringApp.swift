import SwiftUI

@main
struct SaudiColoringApp: App {
    @State private var environment = AppEnvironment.live()

    var body: some Scene {
        WindowGroup {
            HomeView()
                .environment(environment)
        }
    }
}
