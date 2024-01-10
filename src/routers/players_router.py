from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from schema.match import FootballMatch
from schema.player import Player
from schema.team import Team
from bson.json_util import dumps
from database import *
from schema.token import TokenData
import services.rabbitMQ as rabbitMQ
from utils.token_validation import validate_token
from typing import List


# Create a router for team operations
player_router = APIRouter(
    prefix="/players",
    tags=["Players"]
)

@player_router.get("/player/{player_id}", status_code=status.HTTP_202_ACCEPTED, response_model=Player)
async def get_player_by_id(player_id: UUID,current_user: TokenData = Depends(validate_token)):
    try:
        str_player_id = str(player_id)
        player_data = db.players.find_one({"player_id": str_player_id})

        if not player_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")

        return player_data

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Server error: {str(e)}")
    

@player_router.post("/newPlayer/", response_model=Player, status_code=status.HTTP_201_CREATED)
async def create_player(name: str, last_name: str, country: str, age: int, position: str, cost: float, team_id: str, current_user: TokenData = Depends(validate_token)):
    try:
        player_id = str(uuid4())

        new_player = {
            "player_id": player_id,
            "name": name,
            "last_name": last_name,
            "country": country,
            "age": age,
            "position": position,
            "cost": cost,
            "team": team_id,
        }

        existing_player = db.players.find_one({"player_id": player_id})
        if existing_player:
            raise HTTPException(status_code=status.HTTP_207_MULTI_STATUS, detail="Player with this ID already exists")

        inserted = db.players.insert_one(new_player)
        if not inserted.inserted_id:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating player")
        
        rabbitMQ.send_player_created_message(new_player)

        return new_player

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error: {str(e)}")
    

@player_router.get("/searchByTeam/", response_model=List[Player], status_code=status.HTTP_202_ACCEPTED)
async def search_players_by_team(team_id: UUID,current_user: TokenData = Depends(validate_token)):
    try:
        players = list(db.players.find({"team": str(team_id)}))

        if not players:
            return []

        return players

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")




