from fastapi import APIRouter

from api_v1.users import crud
from api_v1.users.schemas import CreateUser

users_router = APIRouter(tags=["Users"])


@users_router.post("/")
async def create_user(user: CreateUser):
    return await crud.create_user_in(user)
