from fastapi import APIRouter, status

from app.core.deps import CurrentUser, OptionalUser
from app.schemas.comment import CommentResponse, CommentsResponse, CreateCommentRequest
from app.services.article import get_article_by_slug
from app.services.comment import (
    build_comment_dto,
    create_comment,
    delete_comment,
    get_comment_by_id,
    get_comments_for_article,
)

router = APIRouter(prefix="/articles/{slug}/comments", tags=["Comments"])


@router.get("", response_model=CommentsResponse)
async def get_comments(slug: str, current_user: OptionalUser) -> CommentsResponse:
    article = await get_article_by_slug(slug)
    comments = await get_comments_for_article(article)
    comment_dtos = [await build_comment_dto(comment, current_user) for comment in comments]
    return CommentsResponse(comments=comment_dtos)


@router.post("", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def add_comment(
    slug: str,
    current_user: CurrentUser,
    request: CreateCommentRequest,
) -> CommentResponse:
    article = await get_article_by_slug(slug)
    comment = await create_comment(article, request.comment.body, current_user)
    return CommentResponse(comment=await build_comment_dto(comment, current_user))


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_comment(slug: str, comment_id: str, current_user: CurrentUser) -> None:
    await get_article_by_slug(slug)
    comment = await get_comment_by_id(comment_id)
    await delete_comment(comment)
