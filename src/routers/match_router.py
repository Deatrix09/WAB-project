from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from bson import json_util
from uuid import UUID
import uuid
from schema.match import FootballMatch  
from schema.token import TokenData  
from utils.token_validation import validate_token
from database import db  

# Create a router for match operations
match_router = APIRouter(
    prefix="/matches",
    tags=["Matches"]
)

@match_router.post("/createMatch/", response_model=FootballMatch, status_code=201)
async def create_match(home_team_id: UUID, away_team_id: UUID, score: str, match_date: datetime, current_user: TokenData = Depends(validate_token)):
    try:
        home_team_doc = db.teams.find_one({"team_id": str(home_team_id)})
        away_team_doc = db.teams.find_one({"team_id": str(away_team_id)})

        if not home_team_doc or not away_team_doc:
            raise HTTPException(status_code=404, detail="One or both teams were not found")

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
            raise HTTPException(status_code=500, detail="Error inserting match into the database")

        return match_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
