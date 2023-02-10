from apidevtools import Schema

from .item import Item


class CategoryBase(Schema):
    __tablename__ = 'category'

    name: str
    description: str = None

    def pretty(self) -> 'Schema':
        self.name = self.name.capitalize()
        return self


class CategoryCreate(CategoryBase):
    ...


class CategoryCreateCrud(CategoryBase):
    user_id: int


class Category(CategoryCreateCrud):
    id: int
    items: list[Item] = []
