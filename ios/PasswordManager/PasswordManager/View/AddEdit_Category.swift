import SwiftUI


struct AddEditCategoryView: View {
    @Environment(\.dismiss) var dismiss
    @EnvironmentObject public var all: PasswordManager
    @EnvironmentObject public var me: User
    @State public var category: Category
    @State public var purpose: String
    private let NAME_LIMIT: Int = 20
    private let DESCRIPTION_LIMIT: Int = 30
    @State private var newName: String = String()
    @State private var newDescription: String = String()
    
    var body: some View {
        VStack(spacing: 0) {
            
            Text((purpose == "EDIT") ?  "Edit category" : "New category")
                .font(.system(size: 45, weight: .bold))
                .padding()
                .padding()
                .frame(width: UIScreen.main.bounds.size.width)
                //.foregroundColor(Color("Main"))
                .background(Color("Foreground"))
                .shadow(color: Color.white.opacity(0.1), radius: 5, x: 0, y: 10)
            MyDivider(c: Color("Background"), w: UIScreen.main.bounds.size.width, h: 10)
            
            Form {
                Section(footer: Text((purpose == "EDIT") ? "" : "Enter a name up to \(NAME_LIMIT) symbols").foregroundColor(.gray)) {
                    TextField(category.name, text: $newName)
                        .autocapitalization(.words)
                        .onChange(of: newName, perform: { _ in self.newName = String(self.newName.prefix(NAME_LIMIT))})
                }
                Section(footer: Text((purpose == "EDIT") ? "" : "Enter a description up to \(DESCRIPTION_LIMIT) symbols (optional)").foregroundColor(.gray)) {
                    TextField((category.description == "") ? "Description:" : category.description, text: $newDescription)
                        .autocapitalization(.none)
                        .disableAutocorrection(true)
                        .onChange(of: newDescription, perform: { _ in self.newDescription = String(self.newDescription.prefix(DESCRIPTION_LIMIT))})
                }
            }
            .onAppear {
                UITableView.appearance().backgroundColor = .clear
            }
            .frame(width: UIScreen.main.bounds.size.width, height: UIScreen.main.bounds.size.height/3, alignment: .leading)
            .background(Color("Foreground"))

            Spacer()
            
            Button(action: { 
                if purpose == "EDIT" {
                    all.changeCategory(of: me, by: category, with: Category(name: (newName.count == 0) ? category.name : newName, description: (newDescription.count == 0) ? category.description : newDescription))
                }
                else {
                    if newName.count != 0 {
                        all.addCategory(of: me, category: Category(name: newName, description: newDescription))
                    }
                }
                dismiss()
            }) {
                Text((purpose == "ADD") ? "Add" : "Save")
                    .foregroundColor(.white)
                    .font(.system(size: 25, weight: .bold))
                    .fontWeight(.bold)
                    .padding(.vertical)
                    .padding(.horizontal, 50)
                    .background(Color("Main"))
                    .clipShape(Capsule())
            }
            .offset(y: -30)
            
            Image(systemName: "lock.circle.fill")
                .resizable()
                .foregroundColor(Color("Main"))
                .frame(width: 150, height: 150)
                .padding(.vertical, 100)
                .opacity(0.5)
                
        }
        .background(Color("Background"))
    }
}
