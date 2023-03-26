from fastapi import APIRouter, HTTPException
import string
import random

from .. import schemas


router = APIRouter(tags=['Password'])


@router.get('/generate/', name='Generate password', response_model=schemas.Password)
def _(length: int = 20,
      uppercase: str = string.ascii_uppercase, lowercase: str = string.ascii_lowercase,
      digits: str = string.digits, specials: str = string.punctuation, discarded: str = '"\'/\\<>;:&%@$'):
    symsets = [cs for s in [uppercase, lowercase, digits, specials] if len(cs := ''.join(set(s).difference(set(discarded))))]
    if not len(symsets):
        raise HTTPException(status_code=400, detail='No symbols to generate a password from given arguments')
    random.shuffle(symsets)
    password = ''
    for i in range(len(symsets) - 1):
        for _ in range(length // len(symsets)):
            password += random.choice(symsets[i])
    while len(password) != length:
        password += random.choice(symsets[-1])
    password = ''.join(random.sample(password, len(password)))
    # pass None if not len(someset) else someset
    return schemas.Password(
        password=password, length=length,
        uppercase=uppercase, lowercase=lowercase,
        digits=digits, special=specials, discarded=discarded
    )
