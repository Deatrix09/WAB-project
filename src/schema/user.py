from pydantic import BaseModel
from typing import Optional


class UserInDB(BaseModel):
    username: str
    hashed_password: str
