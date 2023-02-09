import SwiftUI
import Combine

//should be a database connection with json
let user: User = example()

@main
struct PasswordManagerApp: App {
    @StateObject public var all: PasswordManager = PasswordManager(user)
    @StateObject public var me: User = user
    
    var body: some Scene {
        WindowGroup {
            HomeView()
                .environmentObject(all)
                .environmentObject(me)
                .preferredColorScheme(.dark)
        }
    }
}
