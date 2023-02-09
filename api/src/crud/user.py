from apidevtools import Hasher, Avatar

from .. import schemas
from ..database import db


async def create_user(user: schemas.UserCreate) -> schemas.User:
    user.password = Hasher.hash(password=user.password)
    if not user.avatar_url:
        user.avatar_url = await Avatar.default().url()
    db_user = await db.insert(user, schemas.User)
    return db_user


async def get_user(user_id: int = None, email: str = None, schema: type = schemas.User) -> schemas.User | None:
    field, value = ('email', email) if email else ('id', user_id)
    query, args = f'SELECT * FROM "user" WHERE "{field}" = $1;', (value, )
    db_user = (await db.select(query, args, schema)).first()
    return db_user


async def update_user(user_id: int, user: schemas.UserUpdate) -> schemas.User:
    db_user = await db.update(user, dict(id=user_id), schemas.User)
    return db_user


async def delete_user(user_id: int) -> None:
    query, args = f'DELETE FROM "user" WHERE "id" = $1;', (user_id, )
    await db.execute(query, args)
