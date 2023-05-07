from apidevtools.utils import INF

from .. import schemas
from ..misc import db


async def create_category(category: schemas.CategoryCreate) -> schemas.Category:
    db_category = await db.insert(category, schemas.Category)
    return db_category


async def get_category(category_id: int = None, title: str = None, schema: type = schemas.Category)\
        -> schemas.Category | None:
    field, value = ('id', category_id) if category_id else ('title', title)
    query, args = f'SELECT * FROM "category" WHERE "{field}" = $1;', (value, )
    db_category = await (await db.select(query, args, schema, rel_depth=2)).first()
    return db_category


async def get_categories(limit: int = INF, offset: int = 0, schema: type = schemas.Category) -> list[schemas.Category]:
    query, args = f'SELECT * FROM "category" ORDER BY "is_favourite" DESC, "title", "description" LIMIT $1 OFFSET $2;', (limit, offset)
    db_categories = await (await db.select(query, args, schema, rel_depth=2)).all()
    return db_categories


async def update_category(category_id: int, category: schemas.CategoryCreate) -> schemas.Category:
    db_category = await (await db.update(category, dict(id=category_id), schemas.Category, rel_depth=2)).first()
    return db_category


async def delete_category(category_id: int) -> schemas.Category:
    db_category = await (await db.delete(dict(id=category_id), schemas.Category, 'category')).first()
    return db_category
