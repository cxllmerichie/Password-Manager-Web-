from typing import Optional
from pydantic import Field
from apidevtools.simpleorm import Schema, Relation
from apidevtools.media import imgproc

from .item import Item
from ..const import images


class CategoryBase(Schema):
    __tablename__ = 'category'

    icon: Optional[str | bytes] = Field(default=None)
    name: str = Field(default=..., min_length=1, max_length=20)
    description: Optional[str] = Field(default=None, max_length=50)
    is_favourite: bool = Field(default=False)

    async def into_db(self) -> Schema:
        self.name = self.name.capitalize()
        if not self.icon:
            text = self.name[0]
            if not (icon := await images.get(text)):
                icon = imgproc.default(text).bytes
                await images.set(text, icon)
            self.icon = icon
        return self

    async def from_db(self) -> Schema:
        self.icon = str(self.icon)
        return self


class CategoryCreate(CategoryBase):
    ...


class CategoryCreateCrud(CategoryBase):
    user_id: int = Field(default=...)


class Category(CategoryCreateCrud):
    id: int = Field(default=...)

    items: list[Item] = Field(default=[])

    def relations(self) -> list[Relation]:
        return [
            Relation(Category, 'items', Item, dict(category_id=self.id))
        ]
