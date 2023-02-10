from .. import schemas
from ..database import db


async def create_item(user_id: int, item: schemas.ItemCreate) -> schemas.Item:
    item.user_id = user_id
    db_item = await db.insert(item, schemas.Item)
    return db_item


async def get_item(item_id: int, schema: type = schemas.Item) -> schemas.Item | None:
    query, args = f'SELECT * FROM "item" WHERE "id" = $1;', (item_id, )
    db_user = (await db.select(query, args, schema)).first()
    return db_user


async def get_items(user_id: int, schema: type = schemas.Item) -> schemas.Item:
    query, args = f'SELECT * FROM "item" WHERE "user_id" = $1;', (user_id, )
    db_user = (await db.select(query, args, schema)).all()
    return db_user


async def update_item(item_id: int, item: schemas.ItemCreate) -> schemas.Item:
    db_user = await db.update(item, dict(id=item_id), schemas.Item)
    return db_user


async def delete_item(item_id: int) -> None:
    query, args = f'DELETE FROM "item" WHERE "id" = $1;', (item_id, )
    await db.execute(query, args)
