from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber



class CreateUser(BaseModel):
    username: EmailStr
    phone: PhoneNumber
    password: str
    name: str
    city: str