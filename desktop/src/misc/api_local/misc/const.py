from apidevtools.simpleorm import ORM
from apidevtools.simpleorm.connectors.sqlite import SQLite
from apidevtools.logman import LoggerManager, Logger


SQLITE_DATABASE: str = 'storage'
LOGMAN: LoggerManager = LoggerManager()
LOGGER_SQLITE: Logger = LOGMAN.add('DATABASE', 'logs/database.log')

db = ORM(
    connector=SQLite(
        database=SQLITE_DATABASE
    ),
    logger=LOGGER_SQLITE
)

images = None
keys = None
