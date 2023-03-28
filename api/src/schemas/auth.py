from pydantic import BaseModel, Field, EmailStr

from .user import User


class Token(BaseModel):
    access_token: str = Field(min_length=1)
    token_type: str = Field(min_length=1)


class UserToken(User, Token):
    ...


class UserPayload(BaseModel):
    # email: EmailStr
    email: str
