from logging import Logger
from mysql.connector import connect, Error

from FlaskApp import app


class DataBase:
    logger = Logger(__name__)

    def __init__(self, database: str = 'database.sqlite'):
        self.connection = self.connect(database)

    def connect(self, database: str) -> None:
        try:
            con = connect(database)
            print(type(con))
            return con
        except Error as error:
            warning = f'[DataBase.connect()] {error}'
            self.logger.warning(warning)
        return None

    def execute(self, command: str) -> None:
        try:
            cursor = self.connection.cursor()
            cursor.execute(command)
        except Error as error:
            warning = f'[DataBase.execute()] {error}'
            self.logger.warning(warning)
            print(f'execute({command})')


class PasswordManager:
    def __init__(self):
        self.db = DataBase()
        app.run()