from __future__ import annotations
from sqlalchemy.engine.create import create_engine
from sqlalchemy.schema import Table, Column, MetaData, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.engine.base import Connection
from logging import Logger


class Database:
    logger = Logger(__name__)

    def __init__(self, database: str = 'pypmdb.sqlite'):
        self.meta = MetaData()
        self.tables = self.__tables()
        self.connection = self.connect(database)

    def __tables(self) -> dict[str: Table]:
        return {
            'user': self.user(),
            'category': self.category(),
            'item': self.item(),
            'field': self.field()
        }

    def connect(self, database: str) -> Connection | None:
        try:
            engine = create_engine(f"sqlite:///{database}", echo=True)
            self.meta.create_all(engine)
            return engine.connect()
        except Exception as error:
            self.logger.warning(f'[Database.connect()] {error}')
        return None

    def user(self):
        return Table('User', self.meta,
                     Column('UserID', Integer, primary_key=True),
                     Column('Name', String(50), nullable=False),
                     Column('Surname', String(50), nullable=True),
                     Column('Username', String(50), nullable=False),
                     Column('Password', String(50), nullable=False)
                     )

    def category(self):
        return Table('Category', self.meta,
                     Column('CategoryID', Integer, primary_key=True),
                     Column('Name', String(50), nullable=False),
                     Column('Description', String(50), nullable=True),
                     Column('User_ID', Integer, ForeignKey("User.UserID"))
                     )

    def item(self):
        return Table('Item', self.meta,
                     Column('ItemID', Integer, primary_key=True),
                     Column('Title', String(50), nullable=False),
                     Column('Description', String(50), nullable=True),
                     Column('Category_ID', Integer, ForeignKey("Category.CategoryID"))
                     )

    def field(self):
        return Table('Field', self.meta,
                     Column('FieldID', Integer, primary_key=True),
                     Column('Name', String(50), nullable=False),
                     Column('Value', String(50), nullable=True),
                     Column('Item_ID', Integer, ForeignKey("Item.ItemID"))
                     )
