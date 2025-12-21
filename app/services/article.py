from datetime import datetime, timezone

from beanie import PydanticObjectId

from app.core.exceptions import NotFoundException
from app.models.article import Article
from app.models.user import User
from app.schemas.article import ArticleDto, ArticleForCreateDto, ArticleForUpdateDto
from app.schemas.profile import ProfileDto


def generate_slug(title: str) -> str:
    return "-".join(title.split())


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


async def build_article_dto(article: Article, current_user: User | None) -> ArticleDto:
    author_profile = await get_author_profile(article.author_id, current_user)

    favorited = False
    if current_user and current_user.id in article.favourited_user_ids:
        favorited = True

    return ArticleDto(
        slug=article.slug,
        title=article.title,
        description=article.description,
        body=article.body,
        tagList=article.tag_list,
        favoritesCount=len(article.favourited_user_ids),
        author=author_profile,
        favorited=favorited,
        createdAt=article.created_at,
        updatedAt=article.updated_at,
    )


async def create_article(data: ArticleForCreateDto, author: User) -> Article:
    article = Article(
        title=data.title,
        slug=generate_slug(data.title),
        description=data.description,
        body=data.body,
        tag_list=data.tagList,
        author_id=author.id,
        favourited_user_ids=[author.id],
    )
    await article.insert()

    author.articles_liked_ids.append(article.id)
    await author.save()

    return article


async def get_article_by_slug(slug: str) -> Article:
    article = await Article.find_one(Article.slug == slug)
    if article is None:
        raise NotFoundException("article not found")
    return article


async def update_article(article: Article, data: ArticleForUpdateDto) -> Article:
    update_data = data.model_dump(exclude_unset=True)

    if not update_data:
        return article

    if "title" in update_data:
        article.title = update_data["title"]
        article.slug = generate_slug(update_data["title"])
    if "description" in update_data:
        article.description = update_data["description"]
    if "body" in update_data:
        article.body = update_data["body"]

    article.updated_at = datetime.now(timezone.utc)
    await article.save()
    return article


async def delete_article(article: Article) -> None:
    from app.models.comment import Comment

    await Comment.find(Comment.article_id == article.id).delete()
    await article.delete()


async def favorite_article(article: Article, user: User) -> Article:
    if user.id not in article.favourited_user_ids:
        await article.update({"$addToSet": {"favourited_user_ids": user.id}})
        await user.update({"$addToSet": {"articles_liked_ids": article.id}})
        article.favourited_user_ids.append(user.id)
    return article


async def unfavorite_article(article: Article, user: User) -> Article:
    if user.id in article.favourited_user_ids:
        await article.update({"$pull": {"favourited_user_ids": user.id}})
        await user.update({"$pull": {"articles_liked_ids": article.id}})
        article.favourited_user_ids.remove(user.id)
    return article


async def list_articles(
    current_user: User | None,
    tag: str | None = None,
    author: str | None = None,
    favorited: str | None = None,
    limit: int = 10,
    offset: int = 0,
) -> tuple[list[Article], int]:
    query = {}

    if author:
        author_user = await User.find_one(User.username == author)
        if author_user:
            query["author_id"] = author_user.id
        else:
            return [], 0

    if favorited:
        favorited_user = await User.find_one(User.username == favorited)
        if favorited_user:
            query["favourited_user_ids"] = favorited_user.id
        else:
            return [], 0

    if tag:
        query["tag_list"] = tag

    articles = await Article.find(query).sort(-Article.created_at).skip(offset).limit(limit).to_list()
    total = await Article.find(query).count()

    return articles, total


async def get_feed(user: User, limit: int = 10, offset: int = 0) -> tuple[list[Article], int]:
    if not user.following_ids:
        return [], 0

    query = {"author_id": {"$in": user.following_ids}}
    articles = await Article.find(query).sort(-Article.created_at).skip(offset).limit(limit).to_list()
    total = await Article.find(query).count()

    return articles, total
