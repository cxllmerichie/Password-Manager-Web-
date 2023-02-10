from .. import schemas
from ..database import db


async def create_category(user_id: int, category: schemas.CategoryCreate) -> schemas.Category:
    category.user_id = user_id
    db_category = await db.insert(category, schemas.Category)
    return db_category


async def get_category(category_id: int, schema: type = schemas.Category) -> schemas.Category | None:
    query, args = f'SELECT * FROM "category" WHERE "id" = $1;', (category_id, )
    db_user = (await db.select(query, args, schema)).first()
    return db_user


async def get_categories(user_id: int, schema: type = schemas.Category) -> schemas.Category | None:
    query, args = f'SELECT * FROM "category" WHERE "user_id" = $1;', (user_id, )
    db_user = (await db.select(query, args, schema)).all()
    return db_user


async def update_category(category_id: int, category: schemas.CategoryCreate) -> schemas.Category:
    db_user = await db.update(category, dict(id=category_id), schemas.Category)
    return db_user


async def delete_category(category_id: int) -> None:
    query, args = f'DELETE FROM "category" WHERE "id" = $1;', (category_id, )
    await db.execute(query, args)
