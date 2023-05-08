from apidevtools.utils import INF
from typing import Any

from .. import schemas
from ..misc import db


async def create_category(category: dict[str, Any]) -> dict[str, Any]:
    category = schemas.CategoryCreate(**category)
    db_category = await db.insert(category, schemas.Category)
    return db_category.dict()


async def get_category(category_id: int = None, title: str = None) -> dict[str, Any] | None:
    field, value = ('id', category_id) if category_id else ('title', title)
    query, args = f'SELECT * FROM "category" WHERE "{field}" = $1;', (value, )
    db_category = await (await db.select(query, args, schemas.Category, rel_depth=2)).first()
    return db_category.dict()


async def get_categories(limit: int = INF, offset: int = 0) -> list[dict[str, Any]]:
    query, args = f'SELECT * FROM "category" ORDER BY "is_favourite" DESC, "title", "description" LIMIT $1 OFFSET $2;', (limit, offset)
    db_categories = await (await db.select(query, args, schemas.Category, rel_depth=2)).all()
    return [db_category.dict() for db_category in db_categories]


async def set_category_favourite(category_id: int, is_favourite: bool) -> dict[str, Any]:
    db_category = await (await db.update(dict(is_favourite=is_favourite), dict(id=category_id), schemas.Category, 'category', rel_depth=2)).first()
    return db_category.dict()


async def update_category(category_id: int, category: dict[str, Any]) -> dict[str, Any]:
    category = schemas.CategoryCreate(**category)
    db_category = await (await db.update(category, dict(id=category_id), schemas.Category, rel_depth=2)).first()
    return db_category.dict()


async def delete_category(category_id: int) -> dict[str, Any]:
    db_category = await (await db.delete(dict(id=category_id), schemas.Category, 'category')).first()
    return db_category.dict()
