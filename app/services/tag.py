from app.models.article import Article
from app.schemas.tag import TagWithCount


async def get_all_tags() -> list[TagWithCount]:
    pipeline = [
        {"$unwind": "$tag_list"},
        {"$group": {"_id": "$tag_list", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
    ]
    result = await Article.aggregate(pipeline).to_list()
    return [TagWithCount(tag=item["_id"], count=item["count"]) for item in result]
