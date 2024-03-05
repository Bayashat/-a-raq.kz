from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime
import pytz

class IdMixin:
    id = Column(Integer, primary_key=True)
    

class User(Base, IdMixin):
    __tablename__ = "users"
    
    username = Column(String,unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    
    ads = relationship("Ad", back_populates="user")
    comments = relationship("Comment", back_populates="user")

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
    
    # Relationships
    user = relationship("User", back_populates="ads")
    comments = relationship("Comment", back_populates="ad")
    
    
class Comment(Base, IdMixin):
    __tablename__ = "comments"
    
    created_at = Column(DateTime, default=datetime.now(pytz.timezone('Asia/Almaty')))
    content = Column(Text, nullable=False)
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey('users.id'))
    ad_id = Column(Integer, ForeignKey('ads.id'))
    
    # Relationships
    user = relationship("User", back_populates="comments")
    ad = relationship("Ad", back_populates="comments")
    
    
    
