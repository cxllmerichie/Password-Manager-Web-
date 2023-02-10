from asyncpg.exceptions import UniqueViolationError
from fastapi import HTTPException
from apidevtools import inf, Relation

from .. import schemas
from ..const import db
from .item import get_items, delete_item


async def create_category(user_id: int, category: schemas.CategoryCreate) -> schemas.Category:
    category = schemas.CategoryCreateCrud(**dict(category), user_id=user_id)
    try:
        db_category = await db.insert(category, schemas.Category)
        return db_category
    except UniqueViolationError:
        raise HTTPException(status_code=400, detail=f'Category <{category.name}> already exists')


async def get_category(category_id: int, schema: type = schemas.Category) -> schemas.Category | None:
    query, args = f'SELECT * FROM "category" WHERE "id" = $1;', (category_id, )
    relation = Relation(columns=['*'], tablename='item', where=dict(category_id=category_id), ext_schema_t=schemas.Category, fieldname='items', rel_schema_t=schemas.Item)
    db_category = (await db.select(query, args, schema, [relation])).first()
    return db_category


async def get_categories(user_id: int, limit: int = inf, offset: int = 0, schema: type = schemas.Category) -> list[schemas.Category]:
    query, args = f'SELECT * FROM "category" WHERE "user_id" = $1 LIMIT $2 OFFSET $3;', (user_id, limit, offset)
    db_categories = (await db.select(query, args, schema)).all()
    return db_categories


async def update_category(category_id: int, category: schemas.CategoryCreate) -> schemas.Category:
    db_category = await db.update(category, dict(id=category_id), schemas.Category)
    return db_category


async def delete_category(category_id: int) -> None:
    db_items = await get_items(category_id=category_id, schema=schemas.Item)
    for db_item in db_items:
        await delete_item(item_id=db_item.id)
    query, args = f'DELETE FROM "category" WHERE "id" = $1;', (category_id, )
    await db.execute(query, args)
