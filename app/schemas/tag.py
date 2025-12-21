from pydantic import BaseModel


class TagsResponse(BaseModel):
    tags: list[str]
