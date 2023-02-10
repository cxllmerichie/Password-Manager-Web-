from apidevtools import Schema, Relation

from .field import Field


class ItemBase(Schema):
    __tablename__ = 'item'

    title: str
    description: str = None

    def pretty(self) -> 'Schema':
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
        return [Relation('field', dict(item_id=self.id), Item, 'fields', ['*'], Field)]
