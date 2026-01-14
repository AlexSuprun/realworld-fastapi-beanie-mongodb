from app.models.article import Article
from app.schemas.tag import TagWithCount


async def get_all_tags() -> list[TagWithCount]:
    pipeline = [
        {"$unwind": "$tagList"},
        {"$group": {"_id": "$tagList", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
    ]
    collection = Article.get_pymongo_collection()
    cursor = collection.aggregate(pipeline)
    result = await cursor.to_list(length=None)
    return [TagWithCount(tag=item["_id"], count=item["count"]) for item in result]
