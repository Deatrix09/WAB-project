from typing import List
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from bson import json_util
from uuid import UUID
import uuid
from schema.match import FootballMatch
from schema.team import Team  
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

        current_datetime = datetime.now()
        match_datetime = match_date.replace(second=0, microsecond=0)  # Remove seconds and microseconds for comparison

        if match_datetime > current_datetime:
            # Match is scheduled for the future
            match_status = "Scheduled"
        else:
            # Match has already been played
            match_status = "Played"

        match_data = {
            "match_id": str(uuid.uuid4()),
            "home_team": home_team,
            "away_team": away_team,
            "score": score,
            "date": date_str,
            "time": time_str,
            "status": match_status
        }

        inserted = db.matches.insert_one(match_data)

        if not inserted.inserted_id:
            raise HTTPException(status_code=500, detail="Error inserting match into the database")

        return match_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
    

@match_router.get("/occured", response_model=List[FootballMatch])
async def get_occured_matches():

    past_matches = []

    # Today's date, as a date object
    current_date = datetime.now().date()

    # Query for matches that occurred before today
    matches_cursor = db.matches.find({
        "date": {
            "$lt": current_date.strftime("%Y-%m-%d")
        }
    })

    for match_doc in matches_cursor:
        # Create instances of FootballMatch from the documents
        match = FootballMatch(
            match_id=match_doc["match_id"],
            home_team=Team(**match_doc["home_team"]),
            away_team=Team(**match_doc["away_team"]),
            date=match_doc["date"],
            time=match_doc["time"],
            status=match_doc["status"]
        )
        past_matches.append(match)

    return past_matches

@match_router.get("/upcoming", response_model=List[FootballMatch])
async def get_upcoming_matches():

    past_matches = []

    # Today's date, as a date object
    current_date = datetime.now().date()

    # Query for matches that occurred before today
    matches_cursor = db.matches.find({
        "date": {
            "$gt": current_date.strftime("%Y-%m-%d")
        }
    })

    for match_doc in matches_cursor:
        # Create instances of FootballMatch from the documents
        match = FootballMatch(
            match_id=match_doc["match_id"],
            home_team=Team(**match_doc["home_team"]),
            away_team=Team(**match_doc["away_team"]),
            date=match_doc["date"],
            time=match_doc["time"],
            status=match_doc["status"]
        )
        past_matches.append(match)

    return past_matches