from typing import Optional
from apidevtools.simpleorm import Schema, Relation
from pydantic import Field, EmailStr
from apidevtools.media import imgproc

from .category import Category
from ..const import images


class UserBase(Schema):
    __tablename__ = 'user'

    email: EmailStr
    # email: str
    avatar: Optional[str | bytes] = Field(default=None)

    async def into_db(self) -> Schema:
        self.email = self.email.lower()
        if not self.avatar:
            text = 'Me'
            if not (icon := await images.get(text)):
                icon = imgproc.default(text).bytes
                await images.set(text, icon)
            self.avatar = icon
        return self

    async def from_db(self) -> Schema:
        self.avatar = str(self.avatar)
        return self


class UserCreate(UserBase):
    password: str = Field(default=..., min_length=8, max_length=128)
    # password: str


class UserUpdate(UserBase):
    ...


class User(UserBase):
    id: int = Field(default=...)

    categories: list[Category] = Field(default=[])

    def relations(self) -> list[Relation]:
        return [
            Relation(User, 'categories', Category, dict(user_id=self.id))
        ]
