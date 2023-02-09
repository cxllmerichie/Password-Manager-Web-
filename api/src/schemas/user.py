from apidevtools.simpleorm import Schema
from datetime import datetime


class UserBase(Schema):
    email: str
    avatar_url: str = None

    def name(self) -> str:
        return 'user'

    def pretty(self) -> Schema:
        self.email = self.email.lower()
        return self


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    ...


class User(UserBase):
    id: int
    last_active: datetime
