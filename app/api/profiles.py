from fastapi import APIRouter

from app.core.deps import CurrentUser
from app.schemas.profile import ProfileResponse
from app.services.profile import follow_user, get_profile_by_username, unfollow_user

router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.get("/{username}", response_model=ProfileResponse)
async def get_profile(username: str, current_user: CurrentUser) -> ProfileResponse:
    profile = await get_profile_by_username(username, current_user)
    return ProfileResponse(profile=profile)


@router.post("/{username}/follow", response_model=ProfileResponse)
async def follow(username: str, current_user: CurrentUser) -> ProfileResponse:
    profile = await follow_user(username, current_user)
    return ProfileResponse(profile=profile)


@router.delete("/{username}/follow", response_model=ProfileResponse)
async def unfollow(username: str, current_user: CurrentUser) -> ProfileResponse:
    profile = await unfollow_user(username, current_user)
    return ProfileResponse(profile=profile)
