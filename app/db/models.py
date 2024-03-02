from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship

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
    
    ads = relationship("Ad", back_populates="user")

class Ad(Base, IdMixin):
    __tablename__ = "ads"
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, index=True, nullable=False)
    price = Column(Integer, nullable=False)
    address = Column(String, index=True, nullable=False)
    area = Column(Float, nullable=False)
    rooms_count = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    
    # Foreign key to user
    user_id = Column(Integer, ForeignKey('users.id'))
    
    # Define foreign key relationships
    user = relationship("User", back_populates="ads")
