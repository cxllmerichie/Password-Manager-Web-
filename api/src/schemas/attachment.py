from apidevtools.security import encryptor
from apidevtools.simpleorm import Schema
from uuid import uuid4, UUID
from pydantic import Field
import zlib

from ..const import keys


class AttachmentBase(Schema):
    __tablename__ = 'attachment'

    id: UUID = Field(default_factory=uuid4)
    content: str | bytes = Field(default=..., min_length=1)
    mime: str = Field()
    filename: str = Field(min_length=3)

    async def into_db(self) -> Schema:
        self.content, key = encryptor.encrypt(zlib.compress(eval(self.content)))
        await keys.set(self.id, key)
        return self

    async def from_db(self) -> Schema:
        if key := await keys.get(self.id, convert=True):
            self.content = str(zlib.decompress(encryptor.decrypt(self.content, key, evaluate=True)))
        return self


class AttachmentCreate(AttachmentBase):
    ...


class AttachmentCreateCrud(AttachmentBase):
    item_id: int = Field(default=...)


class Attachment(AttachmentCreateCrud):
    ...
