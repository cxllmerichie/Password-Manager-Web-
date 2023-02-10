from apidevtools import Schema


class FieldBase(Schema):
    __tablename__ = 'field'

    name: str
    value: str
    item_id: int


class FieldCreate(FieldBase):
    ...


class Field(FieldBase):
    ...
