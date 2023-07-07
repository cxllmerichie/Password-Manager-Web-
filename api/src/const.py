from dotenv import load_dotenv
import os
from apidevtools.simpleorm import ORM
from apidevtools.simpleorm.connectors.postgresql import PostgreSQL
from apidevtools import logman
from apidevtools.simpleorm.redis import Redis


assert load_dotenv('.env')

REDIS_HOST: str = os.getenv('REDIS_HOST')
REDIS_PORT: int = int(os.getenv('REDIS_PORT'))
REDIS_USER: str = os.getenv('REDIS_USER', None)
REDIS_PASSWORD: str = os.getenv('REDIS_PASSWORD')

API_HOST: str = os.getenv('API_HOST', '127.0.0.1')
API_PORT: int = int(os.getenv('API_PORT', 8000))

API_TITLE: str = os.getenv('API_TITLE')
API_DESCRIPTION: str = os.getenv('API_DESCRIPTION')
API_VERSION: str = os.getenv('API_VERSION')
API_CONTACT_NAME: str = os.getenv('API_CONTACT_NAME')
API_CONTACT_URL: str = os.getenv('API_CONTACT_URL')
API_CONTACT_EMAIL: str = os.getenv('API_CONTACT_EMAIL')

API_CORS_ORIGINS: list[str] = os.getenv('API_CORS_ORIGINS', '*').split(',')
API_CORS_ALLOW_CREDENTIALS: bool = os.getenv('API_CORS_ALLOW_CREDENTIALS', 'Y')[0].upper() == 'Y'
API_CORS_METHODS: list[str] = os.getenv('API_CORS_METHODS', '*').split(',')
API_CORS_HEADERS: list[str] = os.getenv('API_CORS_HEADERS', '*').split(',')

JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY')
JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM')

LOGGER: logman.Logger = logman.add('logs/api.log')

db = ORM(
    connector=PostgreSQL(
        database=os.getenv('POSTGRESQL_DATABASE'),
        host=os.getenv('POSTGRESQL_HOST'),
        port=int(os.getenv('POSTGRESQL_PORT')),
        user=os.getenv('POSTGRESQL_USER'),
        password=os.getenv('POSTGRESQL_PASSWORD'),
    ),
    logger=logman.add('logs/database.log')
)

keys = Redis(
    database=int(os.getenv('REDIS_KEYS_DATABASE')),
    host=REDIS_HOST,
    port=REDIS_PORT,
    user=REDIS_USER,
    password=REDIS_PASSWORD,
    logger=logman.add('logs/keys.log')
)

images = Redis(
    database=int(os.getenv('REDIS_IMAGES_DATABASE')),
    host=REDIS_HOST,
    port=REDIS_PORT,
    user=REDIS_USER,
    password=REDIS_PASSWORD,
    logger=logman.add('logs/images.log')
)
