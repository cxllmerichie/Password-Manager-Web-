import Foundation


extension String {
    func containsDigit() -> Bool {
        for character in self {
            if character.isNumber {
                return true
            }
        }
        return false
    }
    
    func containsUppercase() -> Bool {
        for character in self {
            if character.isUppercase {
                return true
            }
        }
        return false
    }
    
    func containsLowercase() -> Bool {
        for character in self {
            if character.isLowercase {
                return true
            }
        }
        return false
    }
    
    func containsSpecial() -> Bool {
        for character in self {
            if character.isMathSymbol || character.isPunctuation {
                return true
            }
        }
        return false
    }
    
    func containsWhitespace() -> Bool {
        for character in self {
            if character.isWhitespace {
                return true
            }
        }
        return false
    }
    
    func validAsLogin() -> Bool  {
        return self.count >= 8 && !self.containsWhitespace() && (self.containsLowercase() || self.containsUppercase())
    }
    
    func validAsPassword() -> Bool {
        return self.count >= 8 && self.containsDigit() && self.containsLowercase() && self.containsUppercase() && self.containsSpecial() && !self.containsWhitespace()
    }
    
    func titled() -> String {
        return self.prefix(1).capitalized + self.dropFirst()
    }
    
}


func validateSignUp(_ login: String, _ password: String, _ confpass: String) -> Bool {
    return login.validAsLogin() && password == confpass && password.validAsPassword()
}
