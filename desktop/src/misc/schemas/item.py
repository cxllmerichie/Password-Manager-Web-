from typing import Optional
from apidevtools.simpleorm import Schema, Relation
from datetime import datetime
from apidevtools.media import imgproc
from pydantic import Field
from apidevtools.utils import now_tz_naive
from contextlib import suppress
import zlib

from . import field
from .attachment import Attachment
from ..const import db


class ItemBase(Schema):
    __tablename__ = 'item'
    __noupdate__ = ['created_at']

    icon: Optional[str | bytes] = Field(default=None)
    title: str = Field(default=..., min_length=1, max_length=50)
    description: Optional[str] = Field(default=None, max_length=250)
    expires_at: Optional[datetime] | str = Field(default=None)
    modified_at: datetime | str = Field(default=None)
    created_at: datetime | str = Field(default=None)
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
            with suppress(Exception):
                self.icon = imgproc.crop(self.icon).bytes
        # self.icon = zlib.compress(self.icon)
        if not self.created_at:
            self.created_at = now_tz_naive()
        return self

    async def from_db(self) -> Schema:
        # self.icon = str(zlib.decompress(self.icon))
        return self


class ItemCreate(ItemBase):
    ...


class ItemCreateCrud(ItemBase):
    category_id: int = Field(default=...)


class Item(ItemCreateCrud):
    id: int = Field(default=...)

    fields: list[field.Field] = Field(default=[])
    attachments: list[Attachment] = Field(default=[])

    def relations(self) -> list[Relation]:
        return [
            Relation(Item, 'fields', field.Field, dict(item_id=self.id)),
            Relation(Item, 'attachments', Attachment, dict(item_id=self.id))
        ]
