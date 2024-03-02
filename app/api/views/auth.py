from jose import jwt

from fastapi import APIRouter, Form, Response, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db.models import User
from app.api.repositories.users import UsersRepository
from app.api.serializers.users import CreateUser

router = APIRouter()
users_repository = UsersRepository()
oath2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")\
    


# JWT part
def create_jwt(user_id: int) -> str:
    body = {"user_id": user_id}
    token = jwt.encode(body, "flower-secret", algorithm="HS256")
    return token
    
def decode_jwt(token: str) -> int:
    data = jwt.decode(token, "flower-secret", algorithms="HS256") # json
    return data["user_id"]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()

# 1.Registration
@router.post("/users")
def post_signup(
    user: CreateUser,
    db: Session = Depends(get_db),
):
    user_id = users_repository.create_user(db, user)
    
    return Response(status_code=200, content=f"User {user_id} created")


# 2.Login
# @router.post("/login")
# def post_login(
#     username: str = Form(), 
#     password: str = Form(),
#     db: Session = Depends(get_db)
# ):
#     user = users_repository.get_by_email(db, username)
    
#     if user.password == password:
#         token = create_jwt(user.id)
#         return {"access_token": token, "type": "bearer"}
    
#     raise HTTPException(status_code=401, detail="Invalid password")