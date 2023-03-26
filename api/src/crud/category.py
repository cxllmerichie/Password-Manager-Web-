from apidevtools.utils import INF

from .. import schemas
from ..const import db


async def create_category(user_id: int, category: schemas.CategoryCreate) -> schemas.Category:
    category = schemas.CategoryCreateCrud(**dict(category), user_id=user_id)
    db_category = await db.insert(category, schemas.Category)
    return db_category


async def get_category(category_id: int, schema: type = schemas.Category) -> schemas.Category | None:
    query, args = f'SELECT * FROM "category" WHERE "id" = $1;', (category_id, )
    db_category = await (await db.select(query, args, schema, rel_depth=2)).first()
    return db_category


async def get_categories(user_id: int, limit: int = INF, offset: int = 0, schema: type = schemas.Category) -> list[schemas.Category]:
    query, args = f'SELECT * FROM "category" WHERE "user_id" = $1 LIMIT $2 OFFSET $3;', (user_id, limit, offset)
    db_categories = await (await db.select(query, args, schema, rel_depth=2)).all()
    return db_categories


async def update_category(category_id: int, category: schemas.CategoryCreate) -> schemas.Category:
    db_category = await (await db.update(category, dict(id=category_id), schemas.Category)).first()
    return db_category


async def delete_category(category_id: int) -> schemas.Category:
    db_category = await (await db.delete(dict(id=category_id), schemas.Category, 'category')).first()
    return db_category
