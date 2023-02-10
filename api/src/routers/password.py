from string import ascii_lowercase, ascii_uppercase, digits as string_digits, punctuation
from fastapi import APIRouter, Depends, HTTPException
from random import choice, shuffle as shuffle_list
from string_utils import shuffle as shuffle_str


router = APIRouter(tags=['Password'])


@router.get('/generate/', name='Generate password', response_model=dict[str, str])
def _(length: int = 20, symset: str = None, uppercase: bool = True, lowercase: bool = True, digits: bool = True, special: bool = True):
    if symset:
        return dict(password=shuffle_str(''.join([choice(symset) for _ in range(length)])))

    symset = []
    if uppercase:
        symset.append(ascii_uppercase)
    if lowercase:
        symset.append(ascii_lowercase)
    if digits:
        symset.append(string_digits)
    if special:
        symset.append(punctuation)
    shuffle_list(symset)
    subset_size = length // len(symset)
    password = ''
    for i in range(len(symset) - 1):
        for i in range(subset_size):
            password += choice(symset[i])
    while len(password) != length:
        password += choice(symset[-1])
    password = shuffle_str(password)
    return dict(password=password)
