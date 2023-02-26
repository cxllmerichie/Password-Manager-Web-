from apidevtools.security import encryptor
from apidevtools.simpleorm import Schema

from ..const import DB_CRYPTO_KEY


class FieldBase(Schema):
    __tablename__ = 'field'

    name: str | bytes
    value: str | bytes
    iv: bytes | None = None

    def into_db(self) -> Schema:
        self.name, iv = encryptor.encrypt(self.name, DB_CRYPTO_KEY)
        self.value, _ = encryptor.encrypt(self.value, DB_CRYPTO_KEY, iv)
        self.iv = iv
        return self

    def from_db(self) -> Schema:
        self.name = encryptor.decrypt(self.name, DB_CRYPTO_KEY, self.iv).decode()
        self.value = encryptor.decrypt(self.value, DB_CRYPTO_KEY, self.iv).decode()
        self.iv = None
        return self


class FieldCreate(FieldBase):
    ...


class FieldCreateCrud(FieldBase):
    item_id: int


class Field(FieldCreateCrud):
    id: int
