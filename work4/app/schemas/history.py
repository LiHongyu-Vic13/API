from pydantic import BaseModel
from datetime import datetime

class History(BaseModel):
    id: int
    user_id: int
    user_agent: str
    datetime: datetime

    class Config:
        orm_mode = True