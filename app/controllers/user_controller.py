from fastapi import APIRouter, Depends, HTTPException
from app.database import get_session
from ..services import UserService
from ..repositories import UserRepository
from ..schemas import UserSchema, UserCreateEditDTO
from sqlalchemy.ext.asyncio import AsyncSession

user_router = APIRouter(prefix="/user", tags=["User"])

def get_file_service(session: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(session)

@user_router.post("/create")
async def create_user(user: UserCreateEditDTO, user_service: UserService = Depends(get_file_service)):
    creation = await user_service.create_new_user(user)
    return creation

@user_router.get("/{user_id}")
async def get_user_by_id(user_id: int, user_service: UserService = Depends(get_file_service)):
    user = await user_service.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.get("/email/{email}")
async def get_user_by_email(email: str, user_service: UserService = Depends(get_file_service)):
    user = await user_service.get_user_by_email(email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.put("/update/{user_id}")
async def update_user(user_id: int, user_update: UserSchema, user_service: UserService = Depends(get_file_service)):
    success = await user_service.update_user_by_id(user_id, user_update.model_dump())

    if not success:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User updated successfully"}

@user_router.delete("/delete/{user_id}")
async def update_user(user_id: int, user_service: UserService = Depends(get_file_service)):
    deletion = await user_service.user_repo.delete_by_id(user_id)
    if not deletion:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted successfully"}
