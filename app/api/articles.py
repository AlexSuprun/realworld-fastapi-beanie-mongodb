from fastapi import APIRouter, Query, status

from app.core.deps import CurrentUser, OptionalUser
from app.schemas.article import (
    ArticleResponse,
    ArticlesResponse,
    CreateArticleRequest,
    UpdateArticleRequest,
)
from app.services.article import (
    build_article_dto,
    create_article,
    delete_article,
    favorite_article,
    get_article_by_slug,
    get_feed,
    list_articles,
    unfavorite_article,
    update_article,
)

router = APIRouter(prefix="/articles", tags=["Articles"])


@router.get("", response_model=ArticlesResponse)
async def get_articles(
    current_user: OptionalUser,
    tag: str | None = None,
    author: str | None = None,
    favorited: str | None = None,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> ArticlesResponse:
    articles, total = await list_articles(current_user, tag, author, favorited, limit, offset)
    article_dtos = [await build_article_dto(article, current_user) for article in articles]
    return ArticlesResponse(articles=article_dtos, articlesCount=total)


@router.get("/feed", response_model=ArticlesResponse)
async def get_feed_articles(
    current_user: CurrentUser,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> ArticlesResponse:
    articles, total = await get_feed(current_user, limit, offset)
    article_dtos = [await build_article_dto(article, current_user) for article in articles]
    return ArticlesResponse(articles=article_dtos, articlesCount=total)


@router.get("/{slug}", response_model=ArticleResponse)
async def get_article(slug: str, current_user: OptionalUser) -> ArticleResponse:
    article = await get_article_by_slug(slug)
    return ArticleResponse(article=await build_article_dto(article, current_user))


@router.post("", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
async def create_new_article(
    current_user: CurrentUser,
    request: CreateArticleRequest,
) -> ArticleResponse:
    article = await create_article(request.article, current_user)
    return ArticleResponse(article=await build_article_dto(article, current_user))


@router.put("/{slug}", response_model=ArticleResponse)
async def update_existing_article(
    slug: str,
    current_user: CurrentUser,
    request: UpdateArticleRequest,
) -> ArticleResponse:
    article = await get_article_by_slug(slug)
    updated = await update_article(article, request.article)
    return ArticleResponse(article=await build_article_dto(updated, current_user))


@router.delete("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_article(slug: str, current_user: CurrentUser) -> None:
    article = await get_article_by_slug(slug)
    await delete_article(article)


@router.post("/{slug}/favorite", response_model=ArticleResponse)
async def favorite_existing_article(slug: str, current_user: CurrentUser) -> ArticleResponse:
    article = await get_article_by_slug(slug)
    updated = await favorite_article(article, current_user)
    return ArticleResponse(article=await build_article_dto(updated, current_user))


@router.delete("/{slug}/favorite", response_model=ArticleResponse)
async def unfavorite_existing_article(slug: str, current_user: CurrentUser) -> ArticleResponse:
    article = await get_article_by_slug(slug)
    updated = await unfavorite_article(article, current_user)
    return ArticleResponse(article=await build_article_dto(updated, current_user))
