# Create a router for team operations
from fastapi import APIRouter, Depends

from schema.token import TokenData
from utils.token_validation import validate_token


user_router = APIRouter(
    prefix="/user",
    tags=["User"]
)

@user_router.get("/currentUser", response_model=TokenData)
async def get_current_user(current_user:TokenData = Depends(validate_token)):
    return current_user
