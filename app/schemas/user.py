from pydantic import BaseModel, EmailStr


class LoginDto(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    user: LoginDto


class UserForRegistration(BaseModel):
    email: EmailStr
    password: str
    username: str


class RegisterRequest(BaseModel):
    user: UserForRegistration


class UserForUpdate(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
    bio: str | None = None
    image: str | None = None


class UpdateUserRequest(BaseModel):
    user: UserForUpdate


class UserDto(BaseModel):
    email: EmailStr
    token: str
    username: str
    bio: str
    image: str | None = None


class UserResponse(BaseModel):
    user: UserDto
