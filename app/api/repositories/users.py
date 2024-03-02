from fastapi import HTTPException

from sqlite3 import IntegrityError
from sqlalchemy.orm import Session
from app.db.models import User

from app.api.serializers.users import CreateUser, ModifyUser


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
        except Exception as e:
            # Handle exceptions (e.g., database errors, custom exceptions)
            db.rollback()
            raise e
        
        return user.id
    
    @staticmethod
    def get_by_email(db: Session, username: str) -> User:
        user = db.query(User).filter(User.username == username).first()
        
        if user:
            return user
        
        raise HTTPException(status_code=404, detail="User not found")
            
            
    @staticmethod
    def update_user(db: Session, user_id: int, user_data: ModifyUser):
        db_user = db.query(User).filter(User.id == user_id).first()
        
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        else:
            for key, value in user_data.model_dump(exclude_unset=True).items():
                setattr(db_user, key, value)
                
        try:
            db.commit()
            db.refresh(db_user)
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Invalid user data")
        
    
    @staticmethod
    def get_by_id(db: Session, user_id: int) -> User:
        db_user = db.query(User).filter(User.id == user_id).first()
        
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        else:
            return db_user