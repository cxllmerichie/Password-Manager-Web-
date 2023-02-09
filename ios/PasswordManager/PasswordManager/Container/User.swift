import Foundation
import SwiftUI


class User: Identifiable, ObservableObject, Equatable {
    var id: UUID = UUID()
    @Published var login: String
    @Published var password: String
    @Published var categories: [Category] = []
    
    init(login: String, password: String) {
        self.login=login
        self.password=password
    }
    
    func addCategory(_ category: Category) {
        objectWillChange.send()
        categories.append(category)
    }
    
    func removeCategory(_ category: Category) {
        objectWillChange.send()
        if let categoryIndex = categories.firstIndex(of: category) {
            categories.remove(at: categoryIndex)
        }
    }
    
    static func ==(left: User, right: User) -> Bool {
        return left.id == right.id
    }
    
    func getMy(user: User) {
        objectWillChange.send()
        id = user.id
        login = user.login
        password = user.password
        categories = user.categories
    }
    
}
