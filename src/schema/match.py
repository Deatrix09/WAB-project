from datetime import datetime
from datetime import time, date
from uuid import UUID
from pydantic import BaseModel
from schema.team import Team

class FootballMatch(BaseModel):
    match_id : UUID
    home_team: Team
    away_team: Team
    date: date
    time: time
    status: str

