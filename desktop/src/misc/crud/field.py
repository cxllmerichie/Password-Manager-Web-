from uuid import UUID
from typing import Any

from .. import schemas
from ..const import db


async def create_field(item_id: int, field: dict) -> dict[str, Any]:
    field = schemas.FieldCreateCrud(**field, item_id=item_id)
    db_field = await db.insert(field, schemas.Field)
    return db_field.dict()


async def get_fields(item_id: int, schema: type = schemas.Field) -> list[dict[str, Any]]:
    query, args = f'SELECT * FROM "field" WHERE "item_id" = $1;', (item_id, )
    db_fields = await (await db.select(query, args, schema)).all()
    return [f.dict() for f in db_fields]


async def get_field(field_id: UUID, schema: type = schemas.Field) -> dict[str, Any] | None:
    query, args = f'SELECT * FROM "field" WHERE "id" = $1;', (str(field_id), )
    db_field = await (await db.select(query, args, schema)).first()
    return db_field.dict()


async def update_field(field_id: UUID, field: dict) -> dict[str, Any]:
    field['id'] = field_id
    db_field = await (await db.update(schemas.FieldCreate(**field), dict(id=str(field_id)), schemas.Field)).first()
    return db_field.dict()


async def delete_field(field_id: UUID) -> dict[str, Any]:
    db_field = await (await db.delete(dict(id=str(field_id)), schemas.Field, 'field')).first()
    await db.remove(db_field.id)
    return db_field.dict()
