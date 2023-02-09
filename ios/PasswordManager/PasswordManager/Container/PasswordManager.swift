import Foundation
import SwiftUI


class PasswordManager: ObservableObject {
    @Published var users: [User] = []
    
    init(_ user: User?=nil) {
        if user != nil {
            users.append(user!)
        }
    }
    /// \USER manipulation
    func addUser(_ user: User) {
        objectWillChange.send()
        users.append(user)
    }
    
    func getUser(login: String, password: String) -> User? {
        for user in users {
            if user.login==login && user.password==password {
                return user
            }
        }
        return nil
    }
    /// \CATEGORY manipulation
    func addCategory(of user: User, category: Category) {
        if let userIndex = users.firstIndex(of: user) {
            users[userIndex].addCategory(category)
        }
    }
    
    func getGategory(of user: User, by category: Category) -> Category? {
        if let userIndex = users.firstIndex(of: user) {
            if let categoryIndex = users[userIndex].categories.firstIndex(of: category) {
                return users[userIndex].categories[categoryIndex]
            }
        }
        return nil
    }
    
    func changeCategory(of user: User, by category: Category, with newCategory: Category) {
        objectWillChange.send()
        if let userIndex = users.firstIndex(of: user) {
            if let categoryIndex = users[userIndex].categories.firstIndex(of: category) {
                users[userIndex].categories[categoryIndex].update(with: newCategory)
            }
        }
    }
    
    func removeCategory(of user: User, by category: Category) {
        objectWillChange.send()
        if let userIndex = users.firstIndex(of: user) {
            users[userIndex].removeCategory(category)
        }
    }
    /// \ITEM manipulation
    func getItem(of user: User, in category: Category, by item: Item) -> Item? {
        if let userIndex = users.firstIndex(of: user) {
            if let categoryIndex = users[userIndex].categories.firstIndex(of: category) {
                if let itemIndex = users[userIndex].categories[categoryIndex].items.firstIndex(of: item) {
                    return users[userIndex].categories[categoryIndex].items[itemIndex]
                }
            }
        }
        return nil
    }
    
    func addItem(of user: User, in category: Category, _ item: Item) {
        objectWillChange.send()
        if let userIndex = users.firstIndex(of: user) {
            if let categoryIndex = users[userIndex].categories.firstIndex(of: category) {
                users[userIndex].categories[categoryIndex].addItem(item)
            }
        }
    }
    
    func removeItem(of user: User, in category: Category, _ item: Item) {
        objectWillChange.send()
        if let userIndex = users.firstIndex(of: user) {
            if let categoryIndex = users[userIndex].categories.firstIndex(of: category) {
                users[userIndex].categories[categoryIndex].removeItem(item)
            }
        }
    }
    
    func changeItem(of user: User, in category: Category, by item: Item, with newItem: Item) {
        objectWillChange.send()
        if let userIndex = users.firstIndex(of: user) {
            if let categoryIndex = users[userIndex].categories.firstIndex(of: category) {
                if let dataIndex = users[userIndex].categories[categoryIndex].items.firstIndex(of: item) {
                    users[userIndex].categories[categoryIndex].items[dataIndex].update(with: newItem)
                }
            }
        }
    }
    
}
