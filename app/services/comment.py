from beanie import PydanticObjectId

from app.core.exceptions import NotFoundException
from app.models.article import Article
from app.models.comment import Comment
from app.models.user import User
from app.schemas.comment import CommentDto
from app.schemas.profile import ProfileDto


async def get_author_profile(author_id: PydanticObjectId, current_user: User | None) -> ProfileDto:
    author = await User.get(author_id)
    if author is None:
        raise NotFoundException("author not found")

    following = False
    if current_user and author.id in current_user.following_ids:
        following = True

    return ProfileDto(
        username=author.username,
        bio=author.bio,
        image=author.image,
        following=following,
    )


async def build_comment_dto(comment: Comment, current_user: User | None) -> CommentDto:
    author_profile = await get_author_profile(comment.author_id, current_user)

    return CommentDto(
        id=str(comment.id),
        createdAt=comment.created_at,
        updatedAt=comment.updated_at,
        body=comment.body,
        author=author_profile,
    )


async def create_comment(article: Article, body: str, author: User) -> Comment:
    comment = Comment(
        body=body,
        author_id=author.id,
        article_id=article.id,
    )
    await comment.insert()
    return comment


async def get_comments_for_article(article: Article) -> list[Comment]:
    return await Comment.find(Comment.article_id == article.id).to_list()


async def get_comment_by_id(comment_id: str) -> Comment:
    try:
        comment = await Comment.get(PydanticObjectId(comment_id))
    except Exception:
        raise NotFoundException("comment not found")

    if comment is None:
        raise NotFoundException("comment not found")

    return comment


async def delete_comment(comment: Comment) -> None:
    await comment.delete()
