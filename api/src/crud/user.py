from apidevtools.security import hasher

from .. import schemas
from ..const import db


async def create_user(user: schemas.UserCreate) -> schemas.User:
    user.password = hasher.hash(password=user.password)
    db_user = await db.insert(user, schemas.User)
    return db_user


async def get_user(user_id: int = None, email: str = None, schema: type = schemas.User) -> schemas.User | None:
    field, value = ('email', email.lower()) if email else ('id', user_id)
    query, args = f'SELECT * FROM "user" WHERE "{field}" = $1;', (value, )
    db_user = await (await db.select(query, args, schema, rel_depth=3)).first()
    return db_user


async def update_user(user_id: int, user: schemas.UserUpdate) -> schemas.User:
    db_user = await (await db.update(user, dict(id=user_id), schemas.User)).first()
    return db_user


async def delete_user(user_id: int) -> schemas.User:
    db_user = await (await db.delete(dict(id=user_id), schemas.User, 'user')).first()
    return db_user
