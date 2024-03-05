from pydantic import BaseModel


class AddComment(BaseModel):
    content: str