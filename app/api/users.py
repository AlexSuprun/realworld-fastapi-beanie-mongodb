from fastapi import APIRouter

from app.schemas.user import LoginRequest, RegisterRequest, UserResponse
from app.services.auth import build_user_dto, login_user, register_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=UserResponse)
async def register(request: RegisterRequest) -> UserResponse:
    user, token = await register_user(request.user)
    return UserResponse(user=build_user_dto(user, token))


@router.post("/login", response_model=UserResponse)
async def login(request: LoginRequest) -> UserResponse:
    user, token = await login_user(request.user.email, request.user.password)
    return UserResponse(user=build_user_dto(user, token))
