from pydantic import Field as _Field
from apidevtools.security import encryptor
from apidevtools.simpleorm import Schema
from uuid import uuid4, UUID

from ..const import keys, LOGGER_KEYS


class FieldBase(Schema):
    __tablename__ = 'field'

    id: UUID = _Field(default_factory=uuid4)
    name: str | bytes = _Field(default=..., min_length=1)
    value: str | bytes = _Field(default=..., min_length=1)

    async def into_db(self) -> Schema:
        self.name, key = encryptor.encrypt(self.name)
        self.value, _ = encryptor.encrypt(self.value, key)
        LOGGER_KEYS.info(f'New key set for {self.id}')
        return self

    async def from_db(self) -> Schema:
        if key := await keys.get(self.id, convert=True):
            print(key, type(key))
            self.name = encryptor.decrypt(self.name, key, convert=True)
            self.value = encryptor.decrypt(self.value, key, convert=True)
        return self


class FieldCreate(FieldBase):
    ...


class FieldCreateCrud(FieldBase):
    item_id: int = _Field(default=...)


class Field(FieldCreateCrud):
    ...
