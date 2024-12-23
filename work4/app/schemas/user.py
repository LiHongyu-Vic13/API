from pydantic import BaseModel
from ..models.user import User


class UserUpdate(User):
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    refresh_token: str

from pydantic import BaseModel

class TokenData(BaseModel):
    email: str
