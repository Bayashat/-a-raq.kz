from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber



class CreateUser(BaseModel):
    username: EmailStr
    phone: PhoneNumber
    password: str
    name: str
    city: str
    
class ModifyUser(BaseModel):
    username: EmailStr | None = None
    phone: PhoneNumber | None = None
    password: str | None = None
    name: str | None = None
    city: str | None = None
    
class UserReponse(BaseModel):
    id: int
    username: EmailStr
    phone: str
    password: str
    name: str
    city: str