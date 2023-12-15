
# Create a router for team operations
from schema.user import UserInDB
from ..schema.token import Token
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from database import *

from utils.autentication import authenticate_user, create_access_token, get_password_hash


auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

# User registration
@auth_router.post("/register")
def register_user(username: str, password: str):
    hashed_password = get_password_hash(password)
    db.users.insert_one({"username": username, "password": hashed_password})
    return UserInDB(username=username, hashed_password=hashed_password)

# User login
@auth_router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["username"]})
    return Token(access_token=access_token, token_type='Bearer')
