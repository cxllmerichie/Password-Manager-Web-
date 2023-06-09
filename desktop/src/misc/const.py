from apidevtools.simpleorm.connectors.sqlite import SQLite
from apidevtools.simpleorm import ORM
from typing import Any
from asyncio import AbstractEventLoop, get_event_loop
import ast


class ORMNMap(ORM):
    @staticmethod
    def evaluate(value: bytes, convert: bool = True) -> Any:
        if not convert:
            return value
        try:
            return ast.literal_eval(value.decode())
        except ValueError:
            return ast.literal_eval(f'\'{value.decode()}\'')
        except SyntaxError:
            return value.decode()
        except AttributeError:
            return None

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
                return self.evaluate(mapping['value'], convert)
        except Exception as error:
            self.logger.error(error)
            return None

    async def remove(self, key: Any, convert: bool = False) -> bytes | None:
        try:
            if mapping := await (await self.delete(dict(key=key), tablename='map')).first():
                return self.evaluate(mapping['value'], convert)
        except Exception as error:
            self.logger.error(error)
            return None


db = ORMNMap(
    connector=SQLite(
        database='.db'
    )
)

LOOP: AbstractEventLoop = get_event_loop()


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
