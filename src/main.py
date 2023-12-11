from datetime import  datetime, date, time
import json
from uuid import UUID
import uuid
from fastapi import FastAPI, HTTPException
from schema.match import FootballMatch
from schema.team import Team
from bson.json_util import dumps
from .database import *
from bson import json_util


app = FastAPI()


### WORKING ENDPOINTS
@app.get("/teams/{team_id}", response_model=Team)
async def get_team(team_id: UUID):
    str_team_id = str(team_id)

    # Hledání týmu v databázi
    team_data = db.teams.find_one({"team_id": str_team_id})

    # Kontrola, zda byl tým nalezen
    if not team_data:
        raise HTTPException(status_code=404, detail="Tým nenalezen")

    return team_data


@app.get("/all_teams")
async def get_all_teams():
    teams_collection = db.teams.find()
    teams_list = list(teams_collection)
    return json.loads(dumps(teams_list))



@app.post("/matches/", response_model=FootballMatch)
async def create_match(home_team_id: UUID, away_team_id: UUID, score: str, match_date : datetime):
    home_team_doc = db.teams.find_one({"team_id": str(home_team_id)})
    away_team_doc = db.teams.find_one({"team_id": str(away_team_id)})

    if not home_team_doc or not away_team_doc:
        raise HTTPException(status_code=404, detail="Jeden nebo oba týmy nebyly nalezeny")

    #Převedení dokumentů na slovníky (nebo vytvoření Pydantic modelů)
    home_team = json_util.loads(json_util.dumps(home_team_doc))
    away_team = json_util.loads(json_util.dumps(away_team_doc))


    ## TODO take match_date and match_start_time and send it as time and date in match_data
    now = datetime.now()
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