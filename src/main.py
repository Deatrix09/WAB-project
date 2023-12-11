from fastapi import FastAPI

from src.routers.match_router import match_router
from src.routers.team_router import team_router


app = FastAPI()



app.include_router(match_router)
app.include_router(team_router)
