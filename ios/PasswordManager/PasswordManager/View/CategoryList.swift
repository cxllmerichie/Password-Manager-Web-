import SwiftUI


struct CategoryListView: View {
    @EnvironmentObject public var all: PasswordManager
    @EnvironmentObject public var me: User
    @Binding var tab: Int
    @State private var add = false
    @State private var edit = false
    
    var body: some View {
        NavigationView {
            VStack {
                List(all.getUser(login: me.login, password: me.password)!.categories) { category in
                    NavigationLink(destination: ItemListView(category: category)) {
                        HStack {
                            VStack(alignment: .leading, spacing: 5) {
                                Text(category.name)
                                    .font(.system(size: 25, weight: .bold))
                                    .foregroundColor(.white)
                                if category.description != "" {
                                    Text(category.description)
                                        .font(.system(size: 15, weight: .thin))
                                        //.offset(y: 5)
                                }
                                /*MyDivider(c: Color("Main"), w: UIScreen.main.bounds.size.width*0.70, h: 1)
                                    .offset(y: (category.description != nil) ? 10 : 12)*/
                            }
                            Spacer()
                            Image(systemName: "lock")
                                .resizable()
                                .frame(width: 20, height: 30)
                                .foregroundColor(Color("Main"))
                        }
                        //.padding(.bottom, 10)
                    }
                    .swipeActions {
                        Button(action: {all.removeCategory(of: me, by: category)}) {
                            Image(systemName: "trash")
                        }.tint(Color("Main"))
                        
                        Button(action: {self.edit.toggle()}) {
                            Image(systemName: "gear")
                        }.tint(.gray.opacity(0.5))
                    }
                    .listRowBackground(Color("Foreground"))
                    .listRowSeparatorTint(Color("Main"))
                    .sheet(isPresented: $edit) {
                        AddEditCategoryView(category: category, purpose: "EDIT")
                    }
                }
                .environment(\.defaultMinListRowHeight, 80)
                .onAppear {UITableView.appearance().backgroundColor = .clear}
                .navigationBarTitle("Categories")
                
                Button(action: {self.add.toggle()}) {
                    Image(systemName: "plus.circle.fill")
                        .resizable()
                        .frame(width: 50, height: 50, alignment: .center)
                        .foregroundColor(Color("Main"))
                        //.shadow(color: Color.white.opacity(0.1), radius: 5, x: 0, y: 5)
                }.sheet(isPresented: $add) {
                    AddEditCategoryView(category: Category(name: "Name:"), purpose: "ADD")
                }
            }
            .background(Color("Background").ignoresSafeArea())
        }
        .toolbar { EditButton() }
    }
    
    func moveItem(fromOffsets source: IndexSet, toOffset destination: Int) {
        all.getUser(login: me.login, password: me.password)!.categories.move(fromOffsets: source, toOffset: destination)
    }
    
}


struct MyDivider: View {
    @State public var c: Color
    @State public var w: CGFloat
    @State public var h: CGFloat
    @State public var r: CGFloat = 25
    
    var body: some View {
        RoundedRectangle(cornerRadius: r)
            .fill(c)
            .frame(width: self.w, height: self.h)
            .edgesIgnoringSafeArea(.horizontal)
    }
}
