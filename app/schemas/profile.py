from pydantic import BaseModel


class ProfileDto(BaseModel):
    username: str
    bio: str
    image: str | None = None
    following: bool = False


class ProfileResponse(BaseModel):
    profile: ProfileDto
