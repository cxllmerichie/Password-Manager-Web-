from pydantic import BaseModel


class Password(BaseModel):
    password: str
    length: int
