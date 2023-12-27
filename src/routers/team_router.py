from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, date, time
import json
from uuid import UUID
import uuid
from schema.match import FootballMatch
from schema.team import Team
from bson.json_util import dumps
from database import *
from schema.token import TokenData
from utils.token_validation import validate_token

# Create a router for team operations
team_router = APIRouter(
    prefix="/teams",
    tags=["Teams"]
)

@team_router.get("/getTeam/{team_id}", response_model=Team, status_code=200)
async def get_team(team_id: UUID):
    try:
        str_team_id = str(team_id)
        team_data = db.teams.find_one({"team_id": str_team_id})

        if not team_data:
            raise HTTPException(status_code=404, detail="Team not found")

        return team_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@team_router.get("/allTeams", status_code=200)
async def get_all_teams():
    try:
        teams_collection = db.teams.find()
        teams_list = list(teams_collection)
        return json.loads(dumps(teams_list))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@team_router.post("/newTeam/", response_model=Team, status_code=201)
async def create_team(name: str, founded: int, city: str, stadium: str, current_user: TokenData = Depends(validate_token)):
    try:
        team_id = str(uuid.uuid4())

        new_team = {
            "team_id": team_id,
            "name": name,
            "city": city,
            "stadium": stadium,
            "founded": founded,
        }

        existing_team = db.teams.find_one({"team_id": team_id})
        if existing_team:
            raise HTTPException(status_code=400, detail="Team with this ID already exists")

        inserted = db.teams.insert_one(new_team)
        if not inserted.inserted_id:
            raise HTTPException(status_code=500, detail="Error creating team")

        return new_team

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@team_router.delete("/deleteTeam/{team_id}", status_code=202)
async def delete_team(team_id: UUID, current_user: TokenData = Depends(validate_token)):
    try:
        str_team_id = str(team_id)
        deleted = db.teams.delete_one({"team_id": str_team_id})

        if deleted.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Team not found")

        success_message = "Team successfully deleted"
        status_code = 202

    except Exception as e:
        raise HTTPException(status_code=404, detail="Team not found")

    return {"message": success_message, "status_code": status_code}

