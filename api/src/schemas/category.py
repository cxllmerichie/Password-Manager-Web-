from apidevtools import Schema


class CategoryBase(Schema):
    __tablename__ = 'category'

    name: str
    description: str = None
    user_id: int

    def pretty(self) -> 'Schema':
        self.name = self.title.capitalize()
        return self


class CategoryCreate(CategoryBase):
    ...


class Category(CategoryBase):
    ...
