from apidevtools.simpleorm import Schema, Relation
from datetime import datetime

from .field import Field


class ItemBase(Schema):
    __tablename__ = 'item'

    icon: str | bytes = None
    title: str
    description: str = None
    expiration_date: datetime = None
    is_favourite: bool = False

    async def into_db(self) -> Schema:
        self.title = self.title.capitalize()
        return self


class ItemCreate(ItemBase):
    ...


class ItemCreateCrud(ItemBase):
    category_id: int


class Item(ItemCreateCrud):
    id: int

    fields: list[Field] = []

    def relations(self) -> list[Relation]:
        return [Relation(Item, 'fields', Field, dict(item_id=self.id))]
