from pydantic import BaseModel


class CreateAd(BaseModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str


class AdResponse(BaseModel):   
    id: int 
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str
    user_id: int


class ModifyAd(BaseModel):
    type: str | None = None
    price: int | None = None
    address: str | None = None
    area: float | None = None
    rooms_count: int | None = None
    description: str | None = None