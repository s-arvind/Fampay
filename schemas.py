from datetime import datetime
from typing import Optional, Any, List

from pydantic import BaseModel, Field


class Pagination(BaseModel):
    limit: int = Field(10)
    skip: int = Field(0)


class SearchSchema(BaseModel):
    q: str = Field(None)
    publish_after: Optional[datetime] = Field(None)
    type: str = Field(None)
    channel: str = Field(None)
    

class Item(BaseModel):
    _id: str
    type: str
    publishedAt: datetime
    channelId: str
    title: str
    description: str
    thumbnails: Any
    channelTitle: str

class SearchResponse(BaseModel):
    count: int = Field(0)
    data: List[Item] = Field(list())

class ErrorMessage(BaseModel):
    message: str