from pymongo.errors import DuplicateKeyError

from app.core.exceptions import BadRequestException
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
