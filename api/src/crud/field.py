from .. import schemas
from ..database import db


async def create_field(user_id: int, field: schemas.FieldCreate) -> schemas.Field:
    field.user_id = user_id
    db_field = await db.insert(field, schemas.Field)
    return db_field


async def get_field(field_id: int, schema: type = schemas.Field) -> schemas.Field | None:
    query, args = f'SELECT * FROM "field" WHERE "id" = $1;', (field_id, )
    db_user = (await db.select(query, args, schema)).first()
    return db_user


async def get_fields(user_id: int, schema: type = schemas.Field) -> schemas.Field:
    query, args = f'SELECT * FROM "field" WHERE "user_id" = $1;', (user_id, )
    db_user = (await db.select(query, args, schema)).all()
    return db_user


async def update_field(field_id: int, field: schemas.FieldCreate) -> schemas.Field:
    db_user = await db.update(field, dict(id=field_id), schemas.Field)
    return db_user


async def delete_field(field_id: int) -> None:
    query, args = f'DELETE FROM "field" WHERE "id" = $1;', (field_id, )
    await db.execute(query, args)
