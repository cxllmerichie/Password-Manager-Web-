from apidevtools.simpleorm import ORM
from apidevtools.simpleorm.connectors.sqlite import SQLite
from apidevtools.logman import LoggerManager, Logger
from typing import Any
import ast
import asyncio

from . import tables


SQLITE_DATABASE: str = 'storage.sqlite'
LOGMAN: LoggerManager = LoggerManager()
LOGGER_SQLITE: Logger = LOGMAN.add('DATABASE', 'logs/database.log')

db = ORM(
    connector=SQLite(
        database=SQLITE_DATABASE
    ),
    logger=LOGGER_SQLITE
)

asyncio.get_event_loop().run_until_complete(db.create_pool())
asyncio.get_event_loop().run_until_complete(db.execute(tables.sql))


class SQLMap:
    logger = LOGGER_SQLITE

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
                mapping = await (await db.update(dict(key=key, value=value), dict(key=key), tablename='map')).first()
            else:
                mapping = await db.insert(dict(key=key, value=value), tablename='map')
            return mapping['value']
        except Exception as error:
            self.logger.error(error)
        return None

    async def get(self, key: Any, convert: bool = False) -> bytes | None:
        try:
            mapping = await (await db.select(f'SELECT "value" FROM "map" WHERE "key" = "{str(key)}";')).first()
            return self.evaluate(mapping['value'], convert)
        except Exception as error:
            self.logger.error(error)
            return None

    async def delete(self, key: Any, convert: bool = False) -> bytes | None:
        try:
            mapping = await (await db.delete(dict(key=key), tablename='map')).first()
            return self.evaluate(mapping['value'], convert)
        except Exception as error:
            self.logger.error(error)
            return None


images = SQLMap()
keys = SQLMap()
