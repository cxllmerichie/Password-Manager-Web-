import Foundation


func createDataField() -> DataField {
    return DataField(name: "name", value: "value")
}


func createItem() -> [DataField] {
    return [
        createDataField(),
        createDataField(),
        createDataField()
    ]
}


func createCategory() -> Category {
    let category: Category = Category(name: "category", description: "Description of category")
    category.addItem(Item(title: "title", fields: createItem(), description: "description"))
    category.addItem(Item(title: "title", fields: createItem(), description: "description"))
    category.addItem(Item(title: "title", fields: createItem(), description: "description"))
    return category
}


func createUser() -> User {
    let user: User = User(login: "?", password: "?")
    user.addCategory(createCategory())
    user.addCategory(createCategory())
    user.addCategory(createCategory())
    return user
}


func createPasswordManager() -> PasswordManager {
    let passwordManager: PasswordManager = PasswordManager()
    passwordManager.addUser(createUser())
    passwordManager.addUser(createUser())
    passwordManager.addUser(createUser())
    return passwordManager
}


func unit() {
    print("Testing...\n")
    let pm: PasswordManager = createPasswordManager()
    for user in pm.users {
        print("[User]: \"\(user.login)\", \"\(user.password)\"")
        for cat in user.categories {
            print("\t[Category]: \"\(cat.name)\", \"\(cat.description)\"")
            for data in cat.items {
                print("\t\t[Data]: \"\(data.title)\", \"\(data.description)\"")
                for field in data.fields {
                    print("\t\t\t\(field.name) - \(field.value)")
                }
            }
        }
    }
    print("\nFinished.")
}


func example() -> User {
    let user = User(login: "presentation", password: "")
    
    let c1 = Category(name: "Social Networks", description: "Optional description")
    
    let df1 = [
        DataField(name: "username", value: "cxllmerichieorsmthlikethat"),
        DataField(name: "email", value: "cxllmerichie@gmail.com"),
        DataField(name: "password", value: "special#lowerUpper0digit"),
    ]
    
    
    let df2 = [
        DataField(name: "login", value: "roman.lysychkin@gmail.com"),
        DataField(name: "password", value: "special#lowerUpper0digit")
    ]
    
    c1.addItem(Item(title: "Twitter", fields: df2, description: "Optional description"))
    c1.addItem(Item(title: "Pinterest", fields: df2))
    c1.addItem(Item(title: "Facebook", fields: df2, description: "Optional description"))
    c1.addItem(Item(title: "Snapchat", fields: df2))
    c1.addItem(Item(title: "WhatsApp", fields: df2, description: "Optional description"))
    let df4 = [
        DataField(name: "username", value: "cxllmerichie"),
        DataField(name: "password", value: "special#lowerUpper0digit")
    ]
    c1.addItem(Item(title: "Telegram", fields: df4))
    c1.addItem(Item(title: "Reddit", fields: df4))
    c1.addItem(Item(title: "Instagram", fields: df1, description: "Optional description"))
    c1.addItem(Item(title: "Quora", fields: df2))
    user.addCategory(c1)
    
    let c2 = Category(name: "Job")
    let df5 = [
        DataField(name: "username", value: "cxllmerichie"),
        DataField(name: "email", value: "roman.lysychkin@gmail.com"),
        DataField(name: "password", value: "special#lowerUpper0digit")
    ]
    c2.addItem(Item(title: "LinkedIn", fields: df5))
    user.addCategory(c2)
    
    user.addCategory(Category(name: "Samsung", description: "Optional description"))
    user.addCategory(Category(name: "Servers"))
    user.addCategory(Category(name: "JetBrains", description: "Optional description"))
    user.addCategory(Category(name: "Gmail"))
    user.addCategory(Category(name: "University", description: "Optional description"))
    let c3 = Category(name: "Other", description: "Optional description")
    
    let df6 = [
        DataField(name: "username", value: "cxllmerichie"),
        DataField(name: "email", value: "cxllmerichie@gmail.com"),
        DataField(name: "password", value: "special#lowerUpper0digit")
    ]
    c3.addItem(Item(title: "Soundcloud", fields: df6, description: "useless"))
    user.addCategory(c3)
    return user
}
