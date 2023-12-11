from uuid import UUID
from pydantic import BaseModel

class Team(BaseModel):
    team_id: UUID
    name: str
    city: str
    stadium: str
    founded: int

