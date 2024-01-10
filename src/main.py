from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from src.routers.match_router import match_router
from src.routers.team_router import team_router
from src.routers.auth_router import auth_router
from src.routers.user_router import user_router
from src.routers.players_router import player_router



app = FastAPI()


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(match_router)
app.include_router(team_router)
app.include_router(player_router)




