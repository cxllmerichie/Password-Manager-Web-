from apidevtools.security import encryptor
from apidevtools.simpleorm import Schema
from uuid import uuid4, UUID

from ..const import keys


class FieldBase(Schema):
    __tablename__ = 'field'

    id: UUID = uuid4()
    name: str | bytes
    value: str | bytes

    async def into_db(self) -> Schema:
        self.name, key = encryptor.encrypt(self.name)
        self.value, _ = encryptor.encrypt(self.value, key)
        await keys.set(self.id, key)
        return self

    async def from_db(self) -> Schema:
        key = await keys.get(self.id)
        self.name = encryptor.decrypt(self.name, key, convert=True)
        self.value = encryptor.decrypt(self.value, key, convert=True)
        return self


class FieldCreate(FieldBase):
    ...


class FieldCreateCrud(FieldBase):
    item_id: int


class Field(FieldCreateCrud):
    ...
