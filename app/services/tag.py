from app.models.article import Article


async def get_all_tags() -> list[str]:
    pipeline = [
        {"$unwind": "$tag_list"},
        {"$group": {"_id": "$tag_list"}},
        {"$project": {"_id": 0, "tag": "$_id"}},
    ]
    result = await Article.aggregate(pipeline).to_list()
    return [item["tag"] for item in result]
