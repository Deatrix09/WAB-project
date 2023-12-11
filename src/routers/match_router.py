
from fastapi import APIRouter
from datetime import  datetime, date, time
from bson import json_util
from uuid import UUID
import uuid
from fastapi import FastAPI, HTTPException
from schema.match import FootballMatch
from schema.team import Team
from bson.json_util import dumps
from database import *


# Create a router for team operations
match_router = APIRouter(
    prefix="/matches",
    tags=["Matches"]
)

@match_router.post("/createMatch/", response_model=FootballMatch, status_code=201)
async def create_match(home_team_id: UUID, away_team_id: UUID, score: str, match_date: datetime):
    try:
        home_team_doc = db.teams.find_one({"team_id": str(home_team_id)})
        away_team_doc = db.teams.find_one({"team_id": str(away_team_id)})

        if not home_team_doc or not away_team_doc:
            raise HTTPException(status_code=404, detail="Jeden nebo oba týmy nebyly nalezeny")

        home_team = json_util.loads(json_util.dumps(home_team_doc))
        away_team = json_util.loads(json_util.dumps(away_team_doc))

        date_str = match_date.strftime("%Y-%m-%d")
        time_str = match_date.strftime("%H:%M")

        match_data = {
            "match_id": str(uuid.uuid4()),
            "home_team": home_team,
            "away_team": away_team,
            "score": score,
            "date": date_str,
            "time": time_str
        }

        inserted = db.matches.insert_one(match_data)

        if not inserted.inserted_id:
            raise HTTPException(status_code=500, detail="Chyba při vkládání zápasu do databáze")

        return match_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
