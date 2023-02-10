from apidevtools import Schema, Encryptor
from ..const import DB_CRYPTO_KEY


class FieldBase(Schema):
    __tablename__ = 'field'

    name: str
    value: str

    def encrypted(self) -> Schema:
        self.value = Encryptor.decrypt(self.value, Encryptor.key(DB_CRYPTO_KEY))
        return self

    def decrypted(self) -> Schema:
        self.value = Encryptor.decrypt(self.value, Encryptor.key(DB_CRYPTO_KEY))
        return self


class FieldCreate(FieldBase):
    ...


class FieldCreateCrud(FieldBase):
    item_id: int


class Field(FieldCreateCrud):
    id: int
