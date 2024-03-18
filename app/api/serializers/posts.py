from pydantic import BaseModel
from typing import List

class CreatePost(BaseModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str


class PostResponse(BaseModel):   
    id: int 
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str
    user_id: int
    total_comments: int


class ModifyPost(BaseModel):
    type: str | None = None
    price: int | None = None
    address: str | None = None
    area: float | None = None
    rooms_count: int | None = None
    description: str | None = None
    

class SearchResponse(BaseModel):
    id: int
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    
class SearchResultResponse(BaseModel):
    total: int
    objects: List[SearchResponse]