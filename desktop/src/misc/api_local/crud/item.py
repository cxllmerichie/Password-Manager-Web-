from apidevtools.utils import INF, now_tz_naive
from typing import Any

from .. import schemas
from ..misc import db


async def create_item(category_id: int, item: dict[str, Any]) -> dict[str, Any]:
    item = schemas.ItemCreateCrud(**item, category_id=category_id)
    db_item = await db.insert(item, schemas.Item)
    return db_item.dict()


async def get_item(item_id: int) -> dict[str, Any] | None:
    query, args = f'SELECT * FROM "item" WHERE "id" = $1;', (item_id, )
    db_item = await (await db.select(query, args, schemas.Item, rel_depth=1)).first()
    return db_item.dict()


async def get_items(category_id: int, limit: int = INF, offset: int = 0) -> list[dict[str, Any]]:
    query, args = f'SELECT * FROM "item" WHERE "category_id" = $1 ORDER BY "is_favourite" DESC, "title", "description" LIMIT $2 OFFSET $3;', (category_id, limit, offset)
    db_items = await (await db.select(query, args, schemas.Item, rel_depth=1)).all()
    return [db_item.dict() for db_item in db_items]


async def set_item_favourite(item_id: int, is_favourite: bool) -> dict[str, Any]:
    db_item = await (await db.update(dict(is_favourite=is_favourite), dict(id=item_id), schemas.Item, 'item', rel_depth=1)).first()
    return db_item.dict()


async def update_item(item_id: int, item: dict[str, Any]) -> dict[str, Any]:
    item = schemas.ItemCreate(**item)
    item.modified_at = now_tz_naive()
    db_item = await (await db.update(item, dict(id=item_id), schemas.Item, rel_depth=1)).first()
    return db_item.dict()


async def delete_item(item_id: int) -> dict[str, Any]:
    db_item = await (await db.delete(dict(id=item_id), schemas.Item, 'item')).first()
    return db_item.dict()
