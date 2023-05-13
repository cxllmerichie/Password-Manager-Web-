from dotenv import load_dotenv
from os import getenv
from apidevtools.simpleorm import ORM
from apidevtools.simpleorm.connectors.postgresql import PostgreSQL
from apidevtools.logman import LoggerManager, Logger
from apidevtools.simpleorm.redis import Redis


assert load_dotenv('.env')

POSTGRESQL_DATABASE: str = getenv('POSTGRESQL_DATABASE')
POSTGRESQL_HOST: str = getenv('POSTGRESQL_HOST')
POSTGRESQL_PORT: int = int(getenv('POSTGRESQL_PORT'))
POSTGRESQL_USER: str = getenv('POSTGRESQL_USER')
POSTGRESQL_PASSWORD: str = getenv('POSTGRESQL_PASSWORD')

REDIS_KEYS_DATABASE: int = int(getenv('REDIS_KEYS_DATABASE'))
REDIS_TOKENS_DATABASE: int = int(getenv('REDIS_TOKENS_DATABASE'))
REDIS_IMAGES_DATABASE: int = int(getenv('REDIS_IMAGES_DATABASE'))
REDIS_HOST: str = getenv('REDIS_HOST')
REDIS_PORT: int = int(getenv('REDIS_PORT'))
REDIS_USER: str = getenv('REDIS_USER', None)
REDIS_PASSWORD: str = getenv('REDIS_PASSWORD')
with open('build/postgres.sql', 'r') as file:
    POSTGRESQL_CREATE_TABLES = file.read()

API_HOST: str = getenv('API_HOST', '127.0.0.1')
API_PORT: int = int(getenv('API_PORT', 8000))

API_TITLE: str = getenv('API_TITLE')
API_DESCRIPTION: str = getenv('API_DESCRIPTION')
API_VERSION: str = getenv('API_VERSION')
API_CONTACT_NAME: str = getenv('API_CONTACT_NAME')
API_CONTACT_URL: str = getenv('API_CONTACT_URL')
API_CONTACT_EMAIL: str = getenv('API_CONTACT_EMAIL')

API_CORS_ORIGINS: list[str] = getenv('API_CORS_ORIGINS', '*').split(',')
API_CORS_ALLOW_CREDENTIALS: bool = getenv('API_CORS_ALLOW_CREDENTIALS', 'Y')[0].upper() == 'Y'
API_CORS_METHODS: list[str] = getenv('API_CORS_METHODS', '*').split(',')
API_CORS_HEADERS: list[str] = getenv('API_CORS_HEADERS', '*').split(',')

JWT_SECRET_KEY: str = getenv('JWT_SECRET_KEY')
JWT_ALGORITHM: str = getenv('JWT_ALGORITHM')

LOGGER_API: Logger = LoggerManager.add('logs/api.log')
LOGGER_POSTGRES: Logger = LoggerManager.add('logs/database.log')
LOGGER_KEYS: Logger = LoggerManager.add('logs/keys.log')
LOGGER_TOKENS: Logger = LoggerManager.add('logs/tokens.log')
LOGGER_IMAGES: Logger = LoggerManager.add('logs/images.log')

db = ORM(
    connector=PostgreSQL(
        database=POSTGRESQL_DATABASE,
        host=POSTGRESQL_HOST,
        port=POSTGRESQL_PORT,
        user=POSTGRESQL_USER,
        password=POSTGRESQL_PASSWORD
    ),
    logger=LOGGER_POSTGRES
)

keys = Redis(
    database=REDIS_KEYS_DATABASE,
    host=REDIS_HOST,
    port=REDIS_PORT,
    user=REDIS_USER,
    password=REDIS_PASSWORD,
    logger=LOGGER_KEYS
)

tokens = Redis(
    database=REDIS_TOKENS_DATABASE,
    host=REDIS_HOST,
    port=REDIS_PORT,
    user=REDIS_USER,
    password=REDIS_PASSWORD,
    logger=LOGGER_TOKENS
)

images = Redis(
    database=REDIS_IMAGES_DATABASE,
    host=REDIS_HOST,
    port=REDIS_PORT,
    user=REDIS_USER,
    password=REDIS_PASSWORD,
    logger=LOGGER_IMAGES
)
