from .. import schemas
from ..const import db


async def create_field(item_id: int, field: schemas.FieldCreate) -> schemas.Field:
    field = schemas.FieldCreateCrud(**dict(field), item_id=item_id)
    db_field = await db.insert(field, schemas.Field)
    return db_field


async def get_field(field_id: int, schema: type = schemas.Field) -> schemas.Field | None:
    query, args = f'SELECT * FROM "field" WHERE "id" = $1;', (field_id, )
    db_field = (await db.select(query, args, schema)).first()
    return db_field


async def get_fields(item_id: int, schema: type = schemas.Field) -> list[schemas.Field]:
    query, args = f'SELECT * FROM "field" WHERE "item_id" = $1;', (item_id, )
    db_fields = (await db.select(query, args, schema)).all()
    return db_fields


async def update_field(field_id: int, field: schemas.FieldCreate) -> schemas.Field:
    db_field = await db.update(field, dict(id=field_id), schemas.Field)
    return db_field


async def delete_field(field_id: int) -> schemas.Field:
    db_field = (await db.delete(dict(id=field_id), schemas.Field, 'field')).first()
    return db_field
