from __future__ import annotations
from sqlalchemy.schema import Table, Column, MetaData, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.engine.create import create_engine
from sqlalchemy.engine.base import Connection, Engine
from logging import Logger


class Database:
    __logger = Logger(__name__)
    __database_path: str

    def __init__(self, database_path: str):
        self.__meta = MetaData()
        self.tables = self.__tables()
        self.__connection: Connection = None
        self.__engine: Engine = None
        self.__database_path = database_path

    def __tables(self) -> dict[str: Table]:
        return {
            'user': self.__user(),
            'category': self.__category(),
            'item': self.__item(),
            'field': self.__field()
        }

    def connect(self) -> None:
        try:
            engine = create_engine(f"sqlite:///{self.__database_path}", echo=True)
            self.__meta.create_all(engine)
            self.__connection = engine.connect()
            self.__engine = engine
        except Exception as error:
            self.__logger.warning(f'[Database.connect()] {error}')

    def disconnect(self):
        try:
            self.__connection.close()
            self.__engine.dispose()
        except Exception as error:
            self.__logger.warning(f'[Database.disconnect()] {error}')

    def execute(self, query: str):
        try:
            self.__connection.execute(query)
        except Exception as error:
            self.__logger.warning(f'[Database.execute()] {error}')

    def __user(self):
        return Table('User', self.__meta,
                     Column('UserID', Integer, primary_key=True),
                     Column('Name', String(50), nullable=False),
                     Column('Surname', String(50), nullable=True),
                     Column('Username', String(50), nullable=False),
                     Column('Password', String(50), nullable=False)
                     )

    def __category(self):
        return Table('Category', self.__meta,
                     Column('CategoryID', Integer, primary_key=True),
                     Column('Name', String(50), nullable=False),
                     Column('Description', String(50), nullable=True),
                     Column('User_ID', Integer, ForeignKey("User.UserID"))
                     )

    def __item(self):
        return Table('Item', self.__meta,
                     Column('ItemID', Integer, primary_key=True),
                     Column('Title', String(50), nullable=False),
                     Column('Description', String(50), nullable=True),
                     Column('Category_ID', Integer, ForeignKey("Category.CategoryID"))
                     )

    def __field(self):
        return Table('Field', self.__meta,
                     Column('FieldID', Integer, primary_key=True),
                     Column('Name', String(50), nullable=False),
                     Column('Value', String(50), nullable=True),
                     Column('Item_ID', Integer, ForeignKey("Item.ItemID"))
                     )
