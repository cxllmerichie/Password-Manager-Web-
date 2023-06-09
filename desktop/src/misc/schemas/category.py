from typing import Optional
from pydantic import Field
from apidevtools.simpleorm import Schema, Relation
from apidevtools.media import imgproc
import zlib

from .item import Item
from ..const import db


class CategoryBase(Schema):
    __tablename__ = 'category'

    icon: Optional[str | bytes] = Field(default=None)
    title: str = Field(default=..., min_length=1, max_length=50)
    description: Optional[str] = Field(default=None, max_length=250)
    is_favourite: bool = Field(default=False)

    async def into_db(self) -> Schema:
        self.title = self.title.capitalize()
        if not self.icon:
            text = self.title[0]
            if not (icon := await db.get(text)):
                icon = imgproc.default(text).bytes
                await db.set(text, icon)
            self.icon = icon
        else:
            self.icon = imgproc.crop(eval(self.icon)).bytes
        # self.icon = zlib.compress(self.icon)
        return self

    async def from_db(self) -> Schema:
        # self.icon = str(zlib.decompress(self.icon))
        self.icon = str(self.icon)
        return self


class CategoryCreate(CategoryBase):
    ...


class Category(CategoryCreate):
    id: int = Field(default=...)

    items: list[Item] = Field(default=[])

    def relations(self) -> list[Relation]:
        return [
            Relation(Category, 'items', Item, dict(category_id=self.id))
        ]
