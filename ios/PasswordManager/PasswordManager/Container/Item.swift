import Foundation
import SwiftUI


struct DataField: Identifiable {
    let id: UUID = UUID()
    var name: String
    var value: String
    
    init(name: String, value: String) {
        self.name=name.titled()
        self.value=value
    }
    
}


class Item: Identifiable, ObservableObject, Equatable {
    var id: UUID = UUID()
    @Published var title: String
    @Published var description: String
    @Published var fields: [DataField] = []

    init(title: String, fields: [DataField]=[], description: String = "") {
        self.title=title.titled()
        self.fields=fields
        self.description=description
    }
    
    func update(with item: Item) {
        objectWillChange.send()
        title=item.title
        fields=item.fields
        description=item.description
    }
    
    func getFields() -> [DataField] {
        var dataFields: [DataField] = []
        dataFields.append(DataField(name: "Title", value: title))
        dataFields.append(contentsOf: fields)
        dataFields.append(DataField(name: "Description", value: description))
        return dataFields
    }
    
    static func ==(left: Item, right: Item) -> Bool {
        return left.title == right.title && left.description == right.description
    }
    
}
