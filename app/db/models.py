from sqlalchemy import Column, Integer, String
from app.db.base import Base

class IdMixin:
    id = Column(Integer, primary_key=True)
    

class User(Base, IdMixin):
    __tablename__ = "users"
    
    username = Column(String,unique=True, nullable=False)
    phone = Column(String, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)