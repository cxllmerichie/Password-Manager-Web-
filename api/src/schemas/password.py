from pydantic import BaseModel


class Password(BaseModel):
    password: str
    length: int
    uppercase: str = None
    lowercase: str = None
    digits: str = None
    specials: str = None
    discarded: str = None
