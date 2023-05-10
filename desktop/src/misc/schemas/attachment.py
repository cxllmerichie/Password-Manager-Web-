from apidevtools.security import encryptor
from apidevtools.simpleorm import Schema
from uuid import uuid4, UUID
from pydantic import Field
import zlib

from ..utils import db


class AttachmentBase(Schema):
    __tablename__ = 'attachment'

    id: str | UUID = Field(default_factory=uuid4)  # see comment in schemas.field
    content: str | bytes = Field(default=..., min_length=1)
    mime: str = Field()
    filename: str = Field(min_length=3)

    async def into_db(self) -> Schema:
        self.id = str(self.id)
        if not (key := await db.get(self.id)):
            await db.set(self.id, key := encryptor.randkey())
        self.content, _ = encryptor.encrypt(zlib.compress(eval(self.content)), key)
        return self

    async def from_db(self) -> Schema:
        if key := await db.get(self.id):
            self.content = str(zlib.decompress(encryptor.decrypt(self.content, key, convert=True)))
        else:
            self.content = 'CORRUPTED'
        return self


class AttachmentCreate(AttachmentBase):
    ...


class AttachmentCreateCrud(AttachmentBase):
    item_id: int = Field(default=...)


class Attachment(AttachmentCreateCrud):
    ...
