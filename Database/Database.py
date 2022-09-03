from __future__ import annotations
from sqlalchemy.schema import Table, Column, MetaData, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.engine.create import create_engine
from sqlalchemy.engine.base import Connection, Engine

from Logger.Logger import log, database


class DataType:
    Username = String(25)
    Password = String(25)
    Name = String(25)
    Surname = String(25)
    Title = String(15)
    Description = String(50)
    FieldName = String(15)
    FieldValue = String(25)


class Database:
    __database_path: str

    @log(database)
    def __init__(self, database_path: str = '../Database/pypmdb.sqlite'):
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

    @log(database)
    def connect(self) -> None:
        engine = create_engine(f"sqlite:///{self.__database_path}", echo=True)
        self.__meta.create_all(engine)
        self.__connection = engine.connect()
        self.__engine = engine

    @log(database)
    def disconnect(self):
        self.__connection.close()
        self.__engine.dispose()

    @log(database)
    def execute(self, query: str):
        self.__connection.execute(query)

    def __user(self):
        return Table('User', self.__meta,
                     Column('UserID', Integer, primary_key=True),
                     Column('Name', DataType.Name, nullable=False),
                     Column('Surname', DataType.Surname, nullable=True),
                     Column('Username', DataType.Username, nullable=False),
                     Column('Password', DataType.Password, nullable=False)
                     )

    def __category(self):
        return Table('Category', self.__meta,
                     Column('CategoryID', Integer, primary_key=True),
                     Column('Name', DataType.Title, nullable=False),
                     Column('Description', DataType.Description, nullable=True),
                     Column('User_ID', Integer, ForeignKey("User.UserID"))
                     )

    def __item(self):
        return Table('Item', self.__meta,
                     Column('ItemID', Integer, primary_key=True),
                     Column('Title', DataType.Title, nullable=False),
                     Column('Description', DataType.Description, nullable=True),
                     Column('Category_ID', Integer, ForeignKey("Category.CategoryID"))
                     )

    def __field(self):
        return Table('Field', self.__meta,
                     Column('FieldID', Integer, primary_key=True),
                     Column('Name', DataType.FieldName, nullable=False),
                     Column('Value', DataType.FieldValue, nullable=True),
                     Column('Item_ID', Integer, ForeignKey("Item.ItemID"))
                     )
