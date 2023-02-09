from random import randint
from string import ascii_lowercase, ascii_uppercase, digits, punctuation


class PasswordGenerator:
    def __init__(self, length: int = 20,
                 has_uppercase: bool = True, has_lowercase: bool = True,
                 has_digits: bool = True, has_special: bool = True):
        self.__password = ''
        self.__length = length
        self.__symbols = self.__set_symbols(has_uppercase, has_lowercase, has_digits, has_special)
        self.__generate()
        self.__shuffle()

    def __set_symbols(self, has_uppercase: bool = True, has_lowercase: bool = True,
                      has_digits: bool = True, has_special: bool = True):
        symbols = []
        if has_uppercase:
            symbols.append(ascii_uppercase)
        if has_lowercase:
            symbols.append(ascii_lowercase)
        if has_digits:
            symbols.append(digits)
        if has_special:
            symbols.append(punctuation)
        return symbols

    def __generate(self):
        for symbol_set in self.__symbols:
            for _ in range(int(self.__length / len(self.__symbols))):
                self.__password += symbol_set[randint(0, len(symbol_set) - 1)]

    def __swap(self, string: str, a: int, b: int):
        if a > b:
            a, b = b, a
        return string[:a] + string[b] + string[a + 1:b] + string[a] + string[b + 1:]

    def __shuffle(self, iterations: int = 40):
        shuffled = self.__password
        for _ in range(iterations):
            a = randint(0, len(shuffled) - 1)
            b = randint(0, len(shuffled) - 1)
            shuffle = randint(0, 1)
            if shuffle:
                shuffled = self.__swap(shuffled, a, b)
        self.__password = shuffled

    def __str__(self):
        return self.__password
