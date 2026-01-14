from pymongo.errors import DuplicateKeyError

from app.core.exceptions import BadRequestException, UnauthorizedException
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserDto, UserForRegistration


async def register_user(data: UserForRegistration) -> tuple[User, str]:
    hashed_password = get_password_hash(data.password)

    user = User(
        email=data.email,
        username=data.username,
        password=hashed_password,
    )

    try:
        await user.insert()
    except DuplicateKeyError:
        raise BadRequestException("email is taken")

    token = create_access_token(str(user.id), user.email)
    return user, token


async def login_user(email: str, password: str) -> tuple[User, str]:
    user = await User.find_one(User.email == email)

    if user is None:
        raise UnauthorizedException("password and email do not match")

    try:
        if not verify_password(password, user.password):
            raise UnauthorizedException("password and email do not match")
    except UnauthorizedException:
        raise
    except Exception:
        raise UnauthorizedException("password and email do not match")

    token = create_access_token(str(user.id), user.email)
    return user, token


def build_user_dto(user: User, token: str) -> UserDto:
    return UserDto(
        email=user.email,
        token=token,
        username=user.username,
        bio=user.bio,
        image=user.image,
    )
