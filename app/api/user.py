from fastapi import APIRouter

from app.core.deps import CurrentUser
from app.core.security import create_access_token
from app.schemas.user import UpdateUserRequest, UserResponse
from app.services.auth import build_user_dto
from app.services.user import update_user

router = APIRouter(prefix="/user", tags=["User"])


@router.get("", response_model=UserResponse)
async def get_current_user(current_user: CurrentUser) -> UserResponse:
    token = create_access_token(str(current_user.id), current_user.email)
    return UserResponse(user=build_user_dto(current_user, token))


@router.put("", response_model=UserResponse)
async def update_current_user(
    current_user: CurrentUser,
    request: UpdateUserRequest,
) -> UserResponse:
    updated_user = await update_user(current_user, request.user)
    token = create_access_token(str(updated_user.id), updated_user.email)
    return UserResponse(user=build_user_dto(updated_user, token))
