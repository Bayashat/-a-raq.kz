from pydantic import BaseModel
from typing import List

class AddComment(BaseModel):
    content: str
    

class CommentResponse(BaseModel):
    id: int
    content: str
    user_id: int
    ad_id: int
    

class CommentListResponse(BaseModel):
    comments: List[CommentResponse]