from typing import Optional
from apidevtools.simpleorm import Schema, Relation
from datetime import datetime
from apidevtools.media import imgproc
from pydantic import Field as _Field

from .field import Field
from ..const import images


class ItemBase(Schema):
    __tablename__ = 'item'

    icon: Optional[str | bytes] = _Field(default=None)
    title: str = _Field(default=..., min_length=1, max_length=20)
    description: Optional[str] = _Field(default=None, max_length=50)
    expiration_date: Optional[datetime] = _Field(default=None)
    is_favourite: bool = _Field(default=False)

    async def into_db(self) -> Schema:
        self.title = self.title.capitalize()
        if not self.icon:
            text = self.title[0]
            if not (icon := await images.get(text)):
                icon = imgproc.default(text).bytes
                await images.set(text, icon)
            self.icon = icon
        return self

    async def from_db(self) -> Schema:
        self.icon = str(self.icon)
        return self


class ItemCreate(ItemBase):
    ...


class ItemCreateCrud(ItemBase):
    category_id: int = _Field(default=...)


class Item(ItemCreateCrud):
    id: int = _Field(default=...)

    fields: list[Field] = _Field(default=[])

    def relations(self) -> list[Relation]:
        return [
            Relation(Item, 'fields', Field, dict(item_id=self.id))
        ]
