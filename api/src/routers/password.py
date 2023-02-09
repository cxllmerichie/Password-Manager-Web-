from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from fastapi import APIRouter, Depends, HTTPException
from random import randint

from .. import crud, schemas


router = APIRouter(tags=['User'])


@router.get('/generate/', response_model=dict[str, str])
def _(length: int = 20, has_uppercase: bool = True, has_lowercase: bool = True, has_digits: bool = True,
      has_special: bool = True):
    symbols = []
    if has_uppercase:
        symbols.append(ascii_uppercase)
    if has_lowercase:
        symbols.append(ascii_lowercase)
    if has_digits:
        symbols.append(digits)
    if has_special:
        symbols.append(punctuation)

    password = ''
    for symbol_set in symbols:
        for _ in range(int(length / len(symbols))):
            password += symbol_set[randint(0, len(symbol_set) - 1)]

    def swap(string: str, a: int, b: int):
        if a > b:
            a, b = b, a
        return string[:a] + string[b] + string[a + 1:b] + string[a] + string[b + 1:]

    for _ in range(len(password)):
        a = randint(0, len(password) - 1)
        b = randint(0, len(password) - 1)
        shuffle = randint(0, 1)
        if shuffle:
            password = swap(password, a, b)

    return password
