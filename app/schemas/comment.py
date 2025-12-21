from datetime import datetime

from pydantic import BaseModel

from app.schemas.profile import ProfileDto


class CommentForCreateDto(BaseModel):
    body: str


class CreateCommentRequest(BaseModel):
    comment: CommentForCreateDto


class CommentDto(BaseModel):
    id: str
    createdAt: datetime
    updatedAt: datetime
    body: str
    author: ProfileDto


class CommentResponse(BaseModel):
    comment: CommentDto


class CommentsResponse(BaseModel):
    comments: list[CommentDto]
