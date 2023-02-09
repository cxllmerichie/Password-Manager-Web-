import SwiftUI


struct AddEditItemView: View {
    @Environment(\.dismiss) var dismiss
    @EnvironmentObject public var all: PasswordManager
    @EnvironmentObject public var me: User
    @State public var category: Category
    @State public var item: Item
    @State public var purpose: String
    @State public var fields: [DataField]
    private let TITLE_LIMIT: Int = 20
    private let DESCRIPTION_LIMIT: Int = 30
    private let FIELD_LIMIT: Int = 15
    @State private var newTitle: String = String()
    @State private var newDescription: String = String()
    
    var body: some View {
        VStack(spacing: 0) {
            Text((purpose == "EDIT") ?  "Edit data" : "New data")
                .font(.system(size: 45, weight: .bold))
                .padding()
                .padding()
                .frame(width: UIScreen.main.bounds.size.width)
                .shadow(color: Color.white.opacity(0.1), radius: 5, x: 0, y: 10)
            MyDivider(c: Color("Background"), w: UIScreen.main.bounds.size.width, h: 10)
            
            Form {
                Section(footer: Text((purpose == "EDIT") ? "" : "Enter a title up to \(TITLE_LIMIT) symbols").foregroundColor(.gray)) {
                    TextField(item.title, text: $newTitle)
                        .autocapitalization(.words)
                        .onChange(of: newTitle, perform: { _ in self.newTitle = String(self.newTitle.prefix(TITLE_LIMIT))})
                }
                
                if purpose == "EDIT" {
                    List($fields) { $field in
                        HStack {
                            TextField("Name", text: $field.name)
                            TextField("Value", text: $field.value)
                                .autocapitalization(.none)
                                .disableAutocorrection(true)
                        }
                    }
                }
                else {
                    VStack {
                        List($fields) { $field in
                            HStack {
                                TextField("Name", text: $field.name)
                                    .autocapitalization(.none)
                                TextField("Value", text: $field.value)
                                    .autocapitalization(.none)
                                    .disableAutocorrection(true)
                            }
                        }
                    }
                    Button(action: {fields.append(DataField(name: "", value: ""))}) {
                        HStack {
                            Text("Add field")
                            Spacer()
                            Image(systemName: "plus.circle.fill")
                                .resizable()
                                .frame(width: 25, height: 25)
                                .opacity(0.5)
                        }
                    }
                }
                
                Section(footer: Text((purpose == "EDIT") ? "" : "Enter a description up to \(DESCRIPTION_LIMIT) symbols (optional)").foregroundColor(.gray)) {
                    TextField((item.description == "") ? "Description:" : item.description, text: $newDescription)
                        .autocapitalization(.none)
                        .disableAutocorrection(true)
                        .onChange(of: newDescription, perform: { _ in self.newDescription = String(self.newDescription.prefix(DESCRIPTION_LIMIT))})
                }
            }
            .onAppear {
                UITableView.appearance().backgroundColor = .clear
            }
            .frame(width: UIScreen.main.bounds.size.width, height: UIScreen.main.bounds.size.height/1.5, alignment: .leading)
            Spacer()
            HStack {
                Button(action: {
                    if purpose == "EDIT" {
                        all.changeItem(of: me, in: category, by: item, with: Item(title: (newTitle.count == 0) ? item.title : newTitle, fields: fields, description: (newDescription.count == 0) ? item.description : newDescription))
                    }
                    else {
                        all.addItem(of: me, in: category, Item(title: (newTitle.count == 0) ? "Default title" : newTitle, fields: fields, description: newDescription))
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
            }
            Spacer()
        }
        .background(Color("Foreground"))
    }
}
