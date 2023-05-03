from apidevtools.security import encryptor
from apidevtools.simpleorm import Schema
from uuid import uuid4, UUID
import pydantic

from ..const import keys


class AttachmentBase(Schema):
    __tablename__ = 'attachment'

    id: UUID = pydantic.Field(default_factory=uuid4)
    content: str | bytes = pydantic.Field()
    mime: str = pydantic.Field()
    filename: str = pydantic.Field(min_length=5)

    async def into_db(self) -> Schema:
        self.content, key = encryptor.encrypt(self.content)
        await keys.set(self.id, key)
        return self

    async def from_db(self) -> Schema:
        if key := await keys.get(self.id, convert=True):
            self.content = encryptor.decrypt(self.content, key, convert=True)
        return self


class AttachmentCreate(AttachmentBase):
    ...


class AttachmentCreateCrud(AttachmentBase):
    item_id: UUID = pydantic.Field(default=...)


class Attachment(AttachmentCreateCrud):
    ...
