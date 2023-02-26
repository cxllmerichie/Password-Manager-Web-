from apidevtools.simpleorm import Schema, Relation

from .item import Item


class CategoryBase(Schema):
    __tablename__ = 'category'

    icon: str | bytes = None
    name: str
    description: str = None
    is_favourite: bool = False

    def into_db(self) -> Schema:
        self.name = self.name.capitalize()
        return self


class CategoryCreate(CategoryBase):
    ...


class CategoryCreateCrud(CategoryBase):
    user_id: int


class Category(CategoryCreateCrud):
    id: int

    items: list[Item] = []

    def relations(self) -> list[Relation]:
        return [Relation('item', dict(category_id=self.id), Category, 'items', Item, ['*'])]
