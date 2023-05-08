from apidevtools.security import encryptor
from apidevtools.simpleorm import Schema
from uuid import uuid4, UUID
import pydantic

from ..misc import keys


class FieldBase(Schema):
    __tablename__ = 'field'


    id: str | UUID = pydantic.Field(default_factory=uuid4)  # `id: UUID | str` is correct way, but when fetching data
    # from database the value is converted starting from most left (to UUID) while we need `str`
    name: str | bytes = pydantic.Field(default=..., min_length=1)
    value: str | bytes = pydantic.Field(default='')

    async def into_db(self) -> Schema:
        self.id = str(self.id)
        if not (key := await keys.get(self.id)):
            await keys.set(self.id, key := encryptor.randkey())
        self.name, _ = encryptor.encrypt(self.name, key)
        self.value, _ = encryptor.encrypt(self.value, key)
        return self

    async def from_db(self) -> Schema:
        if key := await keys.get(self.id):
            self.name = encryptor.decrypt(self.name, key, convert=True)
            self.value = encryptor.decrypt(self.value, key, convert=True)
        else:
            self.name = self.value = 'CORRUPTED'
        return self


class FieldCreate(FieldBase):
    ...


class FieldCreateCrud(FieldBase):
    item_id: int = pydantic.Field(default=...)


class Field(FieldCreateCrud):
    ...
