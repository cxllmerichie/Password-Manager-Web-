import SwiftUI


struct HomeView: View {
    @EnvironmentObject public var all: PasswordManager
    @EnvironmentObject public var me: User
    @State private var tab: Int = 1
    
    var body: some View {
        GeometryReader {_ in
            VStack {
                Image(systemName: "lock.circle.fill")
                    .resizable()
                    .shadow(color: Color.white.opacity(0.1), radius: 5, x: 0, y: 10)
                    .foregroundColor(Color("Main"))
                    .frame(width: 200, height: 200)
                    .offset(y: 45)
                ZStack {
                    SignInView(tab: self.$tab)
                        .zIndex(Double(self.tab))
                    SignUpView(tab: self.$tab)
                }
                Spacer()
            }
            .opacity(self.tab != 2 ? 1 : 0)
            if self.tab == 2 {
                CategoryListView(tab: self.$tab)
            }
        }
        .background(Color("Background").edgesIgnoringSafeArea(.all))
    }
}
