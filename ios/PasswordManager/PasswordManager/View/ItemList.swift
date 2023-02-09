import SwiftUI


struct ItemListView: View {
    @EnvironmentObject public var all: PasswordManager
    @EnvironmentObject public var me: User
    @State public var category: Category
    @State private var titleOnly = true
    @State private var description = false
    @State private var add = false
    @State private var edit = false
    
    var body: some View {
        VStack {
            List(all.getGategory(of: me, by: category)!.items) { item in
                HStack {
                    VStack(alignment: .leading) {
                        let dataFields = item.getFields()
                        HStack(alignment: .top, spacing: 0) {
                            Text("\(dataFields[0].name): ")
                                .foregroundColor(.gray)
                                .fontWeight(.ultraLight)
                            Text(dataFields[0].value)
                                .fontWeight(.heavy)
                        }
                        .padding(.bottom, (!titleOnly) ? 5 : 0)
                        if !titleOnly {
                            ForEach(1..<dataFields.count-1) { index in
                                HStack(alignment: .top, spacing: 0) {
                                    Text("\(dataFields[index].name): ")
                                        //.foregroundColor(Color("Main"))
                                        .foregroundColor(.red)
                                        .fontWeight(.heavy)
                                    Text(dataFields[index].value)
                                        .fontWeight(.semibold)
                                }
                            }
                        }
                        if description {
                            if dataFields[dataFields.count-1].value.count != 0 {
                                HStack(alignment: .top, spacing: 0) {
                                    /*Text("\(dataFields[dataFields.count-1].name): ")
                                        .foregroundColor(.gray)
                                        .fontWeight(.ultraLight)*/
                                    Text(dataFields[dataFields.count-1].value)
                                        .fontWeight(.ultraLight)
                                }
                                .padding(.top, (!titleOnly) ? 5 : 0)
                            }
                        }
                    }
                    //.onTapGesture {}
                    Spacer()
                    Image(systemName: "key")
                        .resizable()
                        .frame(width: 20, height: 30)
                        .foregroundColor(Color("Main"))
                }
                .swipeActions {
                    Button(action: {all.removeItem(of: me, in: category, item)}) {
                        Image(systemName: "trash")
                    }.tint(Color("Main"))
                    
                    Button(action: {self.edit.toggle()}) {
                        Image(systemName: "gear")
                    }.tint(.gray.opacity(0.5))
                }
                .listRowBackground(Color("Foreground"))
                .listRowSeparatorTint(Color("Main"))
                .sheet(isPresented: $edit) {
                    AddEditItemView(category: category, item: item, purpose: "EDIT", fields: all.getItem(of: me, in: category, by: item)!.fields)
                }
            }
            .background(Color("Background").ignoresSafeArea())
            .onAppear {UITableView.appearance().backgroundColor = .clear}
            .navigationBarTitle(category.name)
            .toolbar {
                ToolbarItemGroup {
                    HStack {
                        Toggle(isOn: $titleOnly) {
                            Text("Hide").fontWeight(.bold)
                        }
                        
                        Toggle(isOn: $description) {
                            Text("Description").fontWeight(.bold)
                        }
                    }
                }
            }
            Button(action: {self.add.toggle()}) {
                Image(systemName: "plus.circle.fill")
                    .resizable()
                    .frame(width: 50, height: 50, alignment: .center)
                    .foregroundColor(Color("Main"))
                    //.shadow(color: Color.white.opacity(0.1), radius: 5, x: 0, y: 5)
            }.sheet(isPresented: $add) {
                AddEditItemView(category: category, item: Item(title: "Title:"), purpose: "ADD", fields: [])
            }
        }
        .background(Color("Background").ignoresSafeArea())
        .environment(\.defaultMinListRowHeight, 50)
    }
}
