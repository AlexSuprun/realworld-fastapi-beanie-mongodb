from app.core.exceptions import NotFoundException
from app.models.user import User
from app.schemas.profile import ProfileDto


async def get_profile_by_username(username: str, current_user: User | None) -> ProfileDto:
    user = await User.find_one(User.username == username)
    if user is None:
        raise NotFoundException("user not found")

    following = False
    if current_user and user.id in current_user.following_ids:
        following = True

    return ProfileDto(
        username=user.username,
        bio=user.bio,
        image=user.image,
        following=following,
    )


async def follow_user(username: str, current_user: User) -> ProfileDto:
    target_user = await User.find_one(User.username == username)
    if target_user is None:
        raise NotFoundException("user not found")

    if target_user.id not in current_user.following_ids:
        await current_user.update({"$addToSet": {"following_ids": target_user.id}})
        await target_user.update({"$addToSet": {"followers_ids": current_user.id}})

    return ProfileDto(
        username=target_user.username,
        bio=target_user.bio,
        image=target_user.image,
        following=True,
    )


async def unfollow_user(username: str, current_user: User) -> ProfileDto:
    target_user = await User.find_one(User.username == username)
    if target_user is None:
        raise NotFoundException("user not found")

    if target_user.id in current_user.following_ids:
        await current_user.update({"$pull": {"following_ids": target_user.id}})
        await target_user.update({"$pull": {"followers_ids": current_user.id}})

    return ProfileDto(
        username=target_user.username,
        bio=target_user.bio,
        image=target_user.image,
        following=False,
    )
