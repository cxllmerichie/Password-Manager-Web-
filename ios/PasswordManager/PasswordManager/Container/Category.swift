import Foundation
import SwiftUI


class Category: Identifiable, ObservableObject, Equatable {
    var id: UUID = UUID()
    @Published var name: String
    @Published var items: [Item] = []
    @Published var description: String
    
    init(name: String, description: String = "") {
        self.name=name.titled()
        self.description=description
    }
    
    func addItem(_ item: Item) {
        objectWillChange.send()
        items.append(item)
    }
    
    func update(with category: Category) {
        objectWillChange.send()
        name=category.name
        //items=category.items
        description=category.description
    }
    
    func removeItem(_ item: Item) {
        objectWillChange.send()
        if let dataIndex = items.firstIndex(of: item) {
            items.remove(at: dataIndex)
        }
    }
    
    static func ==(left: Category, right: Category) -> Bool {
        return left.id == right.id
    }
    
}
