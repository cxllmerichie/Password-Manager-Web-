from apidevtools.simpleorm import Schema, Relation
from pydantic import BaseModel

from .category import Category


class UserBase(Schema):
    __tablename__ = 'user'

    email: str

    async def into_db(self) -> Schema:
        self.email = self.email.lower()
        return self


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    ...


class User(UserBase):
    id: int

    categories: list[Category] = []

    def relations(self) -> list[Relation]:
        return [
            Relation(User, 'categories', Category, dict(user_id=self.id))
        ]


class UserToken(BaseModel):
    access_token: str
    token_type: str
    user: User


class UserAuth(BaseModel):
    email: str
