from __future__ import annotations
from logging import Logger
from sqlite3 import Error, connect, Connection

from DatabaseManipulation import create_table, add_column, drop_table, DataType, Null, Constraint
from FlaskApp import app


class DataBase:
    logger = Logger(__name__)

    def __init__(self, database: str = 'database.sqlite'):
        self.connection = self.connect(database)

    def connect(self, database: str) -> Connection | None:
        try:
            return connect(database)
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

    def __init(self):
        self.create_table_field()
        self.create_table_item()
        self.create_table_category()
        self.create_table_user()

    def create_table_user(self):
        self.execute(create_table('user', 'category', Constraint.Foreign))
        self.execute(add_column('user', 'name', DataType.String, Null.No))
        self.execute(add_column('user', 'surname', DataType.String, Null.No))
        self.execute(add_column('user', 'username', DataType.String, Null.No))
        self.execute(add_column('user', 'password', DataType.String, Null.No))
        # self.execute(add_constraint('user', 'category', Constraint.Foreign))

    def create_table_category(self):
        self.execute(create_table('category', 'item', Constraint.Foreign))
        self.execute(add_column('category', 'title', DataType.String, Null.No))
        self.execute(add_column('category', 'description', DataType.String, Null.Yes))
        # self.execute(add_constraint('category', 'item', Constraint.Foreign))

    def create_table_item(self):
        self.execute(create_table('item', 'field', Constraint.Foreign))
        self.execute(add_column('item', 'title', DataType.String, Null.No))
        self.execute(add_column('item', 'description', DataType.String, Null.Yes))
        # self.execute(add_constraint('item', 'field', Constraint.Foreign))

    def create_table_field(self):
        self.execute(create_table('field'))
        self.execute(add_column('field', 'name', DataType.String, Null.No))
        self.execute(add_column('field', 'value', DataType.String, Null.Yes))

    def drop_db(self):
        self.execute(drop_table('field'))
        self.execute(drop_table('item'))
        self.execute(drop_table('category'))
        self.execute(drop_table('user'))


class PasswordManager:
    def __init__(self):
        self.db = DataBase()
        app.run()
