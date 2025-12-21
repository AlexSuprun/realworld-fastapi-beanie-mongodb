from fastapi import APIRouter

from app.schemas.tag import TagsResponse
from app.services.tag import get_all_tags

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.get("", response_model=TagsResponse)
async def get_tags() -> TagsResponse:
    tags = await get_all_tags()
    return TagsResponse(tags=tags)
