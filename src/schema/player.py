from pydantic import BaseModel
from uuid import UUID

class Player(BaseModel):
    player_id: UUID
    name: str
    last_name: str
    country: str
    age: int
    position: str
    cost: float
    team: UUID 

