import SwiftUI


struct SignInView: View {
    @EnvironmentObject public var all: PasswordManager
    @EnvironmentObject public var me: User
    @Binding var tab: Int
    private let CHAR_LIMIT: Int = 20
    @State private var username: String = String()
    @State private var password: String = String()
    
    var body: some View {
        ZStack(alignment: .bottom) {
            VStack {
                HStack {
                    VStack(spacing: 10) {
                        Text("SignIn")
                            .foregroundColor(self.tab == 1 ? .white : .gray)
                            .font(.title)
                            .fontWeight(.bold)
                            .onTapGesture {self.tab=1}
                        Capsule()
                            .fill(self.tab == 1 ? Color.blue : Color.clear)
                            .frame(width: 100, height: 5)
                    }
                    Spacer(minLength: 0)
                }
                .padding(.top, 30)
                
                VStack {
                    HStack(spacing: 15) {
                        Image(systemName: "envelope.fill")
                            .foregroundColor(Color("Main"))
                        TextField("Username", text: $username)
                            .onChange(of: username, perform: { _ in self.username = String(self.username.prefix(CHAR_LIMIT))})
                            .autocapitalization(.none)
                            .disableAutocorrection(true)
                    }
                    Divider().background(Color.white.opacity(0.5))
                }
                .padding(.horizontal)
                .padding(.top, 40)
                
                VStack {
                    HStack(spacing: 15) {
                        Image(systemName: "eye.slash.fill")
                            .foregroundColor(Color("Main"))
                        SecureField("Password", text: $password)
                            .onChange(of: password, perform: { _ in self.password = String(self.password.prefix(CHAR_LIMIT))})
                    }
                    Divider().background(Color.white.opacity(0.5))
                }
                .padding(.horizontal)
                .padding(.top, 30)
                
                HStack(spacing: 0) {
                    Spacer(minLength: 0)
                    Button(action: {}) {
                        Text("Forget password?")
                            .foregroundColor(Color.white.opacity(0.6))
                    }
                }
                .padding(.horizontal)
                .padding(.top, 30)
            }
            .padding()
            .padding(.bottom, 65)
            .background(Color("Foreground"))
            .clipShape(RightShape())
            .contentShape(RightShape())
            .shadow(color: .black.opacity(0.3), radius: 5, x: 0, y: -5)
            .cornerRadius(35)
            .padding(.horizontal, 20)
            
            Button(action: {
                if let user: User = all.getUser(login: self.username, password: self.password) {
                    me.getMy(user: user)
                    self.tab=2
                }
            }) {
                Text("Sing In")
                    .foregroundColor(.white)
                    .fontWeight(.bold)
                    .padding(.vertical)
                    .padding(.horizontal, 50)
                    .frame(width: 200, height: 50)
                    .background(Color("Main"))
                    .clipShape(Capsule())
                    .shadow(color: Color.white.opacity(0.1), radius: 5, x: 0, y: 10)
            }
            .offset(y: 25)
            .opacity(self.tab == 1 ? 1 : 0)
        }
        .opacity(self.tab == 2 ? 0: 1)
    }
}


struct RightShape: Shape {
    func path(in rectangle: CGRect) -> Path {
        return Path {path in
            path.move(to: CGPoint(x: rectangle.width, y: 120))
            path.addLine(to: CGPoint(x: rectangle.width, y: rectangle.height))
            path.addLine(to: CGPoint(x: 0, y: rectangle.height))
            path.addLine(to: CGPoint(x: 0, y: 0))
        }
    }
}
