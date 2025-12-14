from api_v1.users.schemas import CreateUser


async def create_user_in(user_in: CreateUser) -> dict:
    user_in.name = user_in.name.strip().title()
    user = user_in.model_dump()
    return {"message": "User Created Successfully", "user": user}
