from typing import Optional
from apidevtools.simpleorm import Schema, Relation
from datetime import datetime, timezone
from apidevtools.media import imgproc
from pydantic import Field
from uuid import UUID, uuid4
from apidevtools.security import encryptor

from . import field
from ..const import images, keys


def utc() -> datetime:
    return datetime.now(timezone.utc)


def now() -> datetime:
    dt = datetime.now()
    dt.replace(tzinfo=None)
    return dt


class ItemBase(Schema):
    __tablename__ = 'item'

    id: UUID = Field(default_factory=uuid4)
    icon: Optional[str | bytes] = Field(default=None)
    title: str = Field(default=..., min_length=1, max_length=20)
    description: Optional[str] = Field(default=None, max_length=50)
    expires_at: Optional[datetime] = Field(default=None)
    modified_at: datetime = Field(default=None)
    created_at: datetime = Field(default=None)
    attachments: list[str | bytes] = Field(default=[])
    is_favourite: bool = Field(default=False)

    async def into_db(self) -> Schema:
        self.title = self.title.capitalize()
        if not self.icon:
            text = self.title[0]
            if not (icon := await images.get(text)):
                icon = imgproc.default(text).bytes
                await images.set(text, icon)
            self.icon = icon
        if not self.created_at:
            self.created_at = now()
        else:
            self.modified_at = now()
        if len(self.attachments):
            key = await keys.set(self.id, encryptor.randkey())
            self.attachments = [encryptor.encrypt(attachment, key)[0] for attachment in self.attachments]
        return self

    async def from_db(self) -> Schema:
        self.icon = str(self.icon)
        if len(self.attachments):
            key = await keys.get(self.id, convert=True)
            self.attachments = [encryptor.decrypt(attachment, key, convert=True) for attachment in self.attachments]
        return self


class ItemCreate(ItemBase):
    ...


class ItemCreateCrud(ItemBase):
    category_id: int = Field(default=...)


class Item(ItemCreateCrud):
    fields: list[field.Field] = Field(default=[])

    def relations(self) -> list[Relation]:
        return [
            Relation(Item, 'fields', field.Field, dict(item_id=self.id))
        ]
