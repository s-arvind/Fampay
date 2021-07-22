from datetime import datetime
from typing import Optional, Any, List

from pydantic import BaseModel, Field


class Pagination(BaseModel):
    limit: int = Field(10)
    skip: int = Field(0)


# api search query parameter , optional fields
class SearchSchema(BaseModel):
    q: str = Field(None)
    publish_after: Optional[datetime] = Field(None)
    type: str = Field(None)
    channel: str = Field(None)
    

# schema for one document
class Item(BaseModel):
    _id: str
    type: str
    publishedAt: datetime
    channelId: str
    title: str
    description: str
    thumbnails: Any
    channelTitle: str

# search api response schema
class SearchResponse(BaseModel):
    count: int = Field(0)
    data: List[Item] = []

# error schema
class ErrorMessage(BaseModel):
    message: str