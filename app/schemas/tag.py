from pydantic import BaseModel


class TagWithCount(BaseModel):
    tag: str
    count: int


class TagsResponse(BaseModel):
    tags: list[TagWithCount]
