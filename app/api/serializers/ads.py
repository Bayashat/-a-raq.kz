from pydantic import BaseModel


class CreateAd(BaseModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str