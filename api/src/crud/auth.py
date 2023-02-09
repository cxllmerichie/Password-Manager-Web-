from fastapi.security import OAuth2PasswordBearer as OAuth2Bearer
from fastapi import Depends, HTTPException
from os import getenv
from apidevtools import Hasher
import jwt

from apidevtools import utcnow
from .. import schemas
from ..database import db
from .user import get_user


async def authenticate_user(email: str, password: str):
    db_user = await get_user(email=email, schema=schemas.UserCreate)
    if db_user and Hasher.cmp(pw_hash=db_user.password, password=password):
        return db_user
    raise HTTPException(status_code=401, detail=f'Invalid password for user <{db_user.email}>')


async def create_token(user: schemas.User):
    token = jwt.encode(user.serializable(), getenv('JWT_SECRET_KEY'), algorithm='HS256')
    return dict(access_token=token, token_type='bearer')


async def get_current_user(token: str = Depends(OAuth2Bearer(tokenUrl='/auth/token/'))) -> schemas.User:
    try:
        payload = jwt.decode(token, getenv('JWT_SECRET_KEY'), algorithms=['HS256'])
    except Exception:
        raise HTTPException(status_code=401, detail='Authorization error')
    db_user = await get_user(email=payload['email'], schema=schemas.User)
    if not db_user:
        raise HTTPException(status_code=401, detail=f'Unauthorized')
    db_user.last_active = utcnow()
    db_user = await db.update(db_user, dict(id=db_user.id), schemas.User)
    return db_user
