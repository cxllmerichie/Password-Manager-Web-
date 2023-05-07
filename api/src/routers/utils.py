from fastapi import APIRouter, HTTPException
import string
import random

from .. import schemas


router = APIRouter(tags=['Utilities'])


@router.get('/generate/', name='Generate password', response_model=schemas.Password)
def _(length: int = 20,
      uppercase: str | None = string.ascii_uppercase, lowercase: str | None = string.ascii_lowercase,
      digits: str | None = string.digits, specials: str | None = string.punctuation, discarded: str | None = '"\'/\\<>;:&%@$'):
    symsets = [clean_symset for symset in [uppercase, lowercase, digits, specials] if symset and len(clean_symset := ''.join(set(symset).difference(set(discarded))))]
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

    return schemas.Password(password=password, length=length)
