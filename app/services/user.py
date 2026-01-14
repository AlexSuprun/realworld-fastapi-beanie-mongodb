from pymongo.errors import DuplicateKeyError

from app.core.exceptions import BadRequestException, UnauthorizedException
from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserForUpdate


async def update_user(user: User, data: UserForUpdate) -> User:
    update_data = data.model_dump(exclude_unset=True)

    if not update_data:
        return user

    for field, value in update_data.items():
        setattr(user, field, value)

    try:
        await user.save()
    except DuplicateKeyError:
        raise BadRequestException("email or username taken")

    return user


async def change_password(user: User, current_password: str, new_password: str) -> dict:
    try:
        if not verify_password(current_password, user.password):
            raise UnauthorizedException("invalid credentials")
    except UnauthorizedException:
        raise
    except Exception:
        raise UnauthorizedException("invalid credentials")

    hashed_password = get_password_hash(new_password)
    user.password = hashed_password
    await user.save()

    return {"message": "password changed successfully"}
