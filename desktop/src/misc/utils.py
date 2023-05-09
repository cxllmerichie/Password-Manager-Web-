from apidevtools.simpleorm.connectors.sqlite import SQLite
from apidevtools.simpleorm import ORM
from typing import Any, Coroutine
from qcontextapi import CONTEXT
from datetime import datetime
from enum import Enum
import asyncio
import socket
import ast
import os

from .assets import EXTENSIONS


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
            mapping = await (await self.select(f'SELECT "value" FROM "map" WHERE "key" = "{str(key)}";')).first()
            return self.evaluate(mapping['value'], convert)
        except Exception as error:
            self.logger.error(error)
            return None

    async def remove(self, key: Any, convert: bool = False) -> bytes | None:
        try:
            mapping = await (await self.delete(dict(key=key), tablename='map')).first()
            return self.evaluate(mapping['value'], convert)
        except Exception as error:
            self.logger.error(error)
            return None


tables: str = '''
CREATE TABLE IF NOT EXISTS "category" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,

    "icon" BYTEA NOT NULL,
    "title" TEXT NOT NULL UNIQUE,
    "description" TEXT DEFAULT NULL,
    "is_favourite" BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS "item" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,

    "icon" BYTEA NOT NULL,
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

    "name" BYTEA NOT NULL,
    "value" BYTEA NOT NULL,

    "item_id" INTEGER NOT NULL,
    CONSTRAINT fk_item FOREIGN KEY("item_id") REFERENCES "item" ("id")
);

CREATE TABLE IF NOT EXISTS "attachment" (
    "id" TEXT PRIMARY KEY,

    "content" BYTEA NOT NULL,
    "mime" TEXT NOT NULL,
    "filename" TEXT NOT NULL,

    "item_id" INTEGER NOT NULL,
    CONSTRAINT fk_item FOREIGN KEY("item_id") REFERENCES "item" ("id")
);

CREATE TABLE IF NOT EXISTS "map" (
    "key" TEXT,
    "value" BYTEA
);
'''

db = ORMNMap(connector=SQLite(database='storage.db'))


def start_local():
    asyncio.get_event_loop().run_until_complete(db.create_pool())
    asyncio.get_event_loop().run_until_complete(db.execute(tables))
    CONTEXT['local'] = True


def stop_local():
    asyncio.get_event_loop().run_until_complete(db.close_pool())
    CONTEXT['local'] = False


class Storage(Enum):
    LOCAL = 'local'
    REMOTE = 'remote'
    HYBRID = 'hybrid'


def prepare(coroutine: Coroutine) -> Any:
    return asyncio.get_event_loop().run_until_complete(coroutine)


def is_connected():
    try:
        socket.create_connection(('8.8.8.8', 53))
        return True
    except OSError:
        pass
    return False


def icon_name() -> str:
    return f"{datetime.now().strftime('%d.%m.%Y %H-%M-%S')}.{EXTENSIONS.ICON}"


def icon_path() -> str:
    return os.path.join(os.path.abspath('icons'), icon_name())


def save_icon(icon: bytes | str) -> None:
    with open(icon_path(), 'wb') as file:
        file.write(eval(icon))
