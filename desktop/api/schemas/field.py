from apidevtools.security import encryptor
from apidevtools.simpleorm import Schema
from uuid import uuid4, UUID
import pydantic

from ..const import db


class FieldBase(Schema):
    __tablename__ = 'field'

    id: UUID | str = pydantic.Field(default_factory=uuid4)
    name: str | bytes = pydantic.Field(default=..., min_length=1)
    value: str | bytes = pydantic.Field(default=..., min_length=1)

    async def into_db(self) -> Schema:
        self.id = str(self.id)
        self.name, key = encryptor.encrypt(self.name)
        self.value, _ = encryptor.encrypt(self.value, key)
        await db.set(self.id, key)
        return self

    async def from_db(self) -> Schema:
        if key := await db.get(self.id):
            self.name = encryptor.decrypt(self.name, key, convert=True)
            self.value = encryptor.decrypt(self.value, key, convert=True)
        return self


class FieldCreate(FieldBase):
    ...


class FieldCreateCrud(FieldBase):
    item_id: int = pydantic.Field(default=...)


class Field(FieldCreateCrud):
    ...
