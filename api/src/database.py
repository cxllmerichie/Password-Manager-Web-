from dotenv import load_dotenv
from os import getenv
from apidevtools import PostgresqlStorage


ENV = load_dotenv('api/.env')

db = PostgresqlStorage(
    database=getenv('DB_NAME'),
    host=getenv('DB_HOST'),
    port=getenv('DB_PORT'),
    user=getenv('DB_USER'),
    password=getenv('DB_PASS')
)
