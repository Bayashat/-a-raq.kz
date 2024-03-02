from fastapi import HTTPException

from sqlite3 import IntegrityError
from sqlalchemy.orm import Session
from app.db.models import User

from app.api.serializers.users import CreateUser


class UsersRepository:
    @staticmethod
    def create_user(db: Session, user_data: CreateUser) -> int:
        try: 
            # Try to query if the user already exists
            existing_user = db.query(User).filter(User.username == user_data.username).first()
            
            if existing_user:
                raise HTTPException(status_code=400, detail="User already exists")
            
            # If the user does not exist, create a new user object and add it to the database
            user = User(**user_data.model_dump())
            db.add(user)
            db.commit()
            db.refresh(user)
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="User already exists")
        
        return user.id