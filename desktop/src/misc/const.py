from apidevtools.simpleorm.connectors.sqlite import SQLite
from apidevtools.utils import evaluate
from apidevtools.simpleorm import ORM
from typing import Any


class ORMNMap(ORM):
    async def set(self, key: Any, value: Any) -> Any:
        try:
            if exists := await self.get(key):
                mapping = await (await self.update(dict(key=key, value=value), dict(key=key), tablename='map')).first()
            else:
                mapping = await self.insert(dict(key=key, value=value), tablename='map')
            return mapping['value']
        except Exception as error:
            self.logger.error(error)
        return None

    async def get(self, key: Any, convert: bool = False) -> bytes | None:
        try:
            if mapping := await (await self.select(f'SELECT "value" FROM "map" WHERE "key" = "{str(key)}";')).first():
                return evaluate(mapping['value'], convert)
        except Exception as error:
            self.logger.error(error)
            return None

    async def remove(self, key: Any, convert: bool = False) -> bytes | None:
        try:
            if mapping := await (await self.delete(dict(key=key), tablename='map')).first():
                return evaluate(mapping['value'], convert)
        except Exception as error:
            self.logger.error(error)
            return None


db = ORMNMap(
    connector=SQLite(
        database='.db'
    )
)


tables: str = '''
CREATE TABLE IF NOT EXISTS "category" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,

    "icon" BLOB NOT NULL,
    "title" TEXT NOT NULL UNIQUE,
    "description" TEXT DEFAULT NULL,
    "is_favourite" BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS "item" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,

    "icon" BLOB NOT NULL,
    "title" TEXT NOT NULL,
    "description" TEXT DEFAULT NULL,
    "expires_at" TIMESTAMP DEFAULT NULL,
    "modified_at" TIMESTAMP DEFAULT NULL,
    "created_at" TIMESTAMP NOT NULL,
    "is_favourite" BOOLEAN DEFAULT FALSE,

    "category_id" INTEGER NOT NULL,
    CONSTRAINT fk_category FOREIGN KEY("category_id") REFERENCES "category" ("id")
);

CREATE TABLE IF NOT EXISTS "field" (
    "id" TEXT PRIMARY KEY,

    "name" BLOB NOT NULL,
    "value" BLOB NOT NULL,

    "item_id" INTEGER NOT NULL,
    CONSTRAINT fk_item FOREIGN KEY("item_id") REFERENCES "item" ("id")
);

CREATE TABLE IF NOT EXISTS "attachment" (
    "id" TEXT PRIMARY KEY,

    "content" BLOB NOT NULL,
    "mime" TEXT NOT NULL,
    "filename" TEXT NOT NULL,

    "item_id" INTEGER NOT NULL,
    CONSTRAINT fk_item FOREIGN KEY("item_id") REFERENCES "item" ("id")
);

CREATE TABLE IF NOT EXISTS "map" (
    "key" TEXT PRIMARY KEY,
    "value" BLOB NOT NULL
);
'''
