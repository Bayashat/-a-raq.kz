from jose import jwt
from typing import List
from fastapi import APIRouter, Form, Response, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db.models import User
from app.api.repositories.users import UsersRepository
from app.api.serializers.users import CreateUser, ModifyUser, UserReponse, ShanyrakItem, FavoriteShanyrak

router = APIRouter()
users_repository = UsersRepository()
oath2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/users/login")
    


# JWT part
def create_jwt(user_id: int) -> str:
    body = {"user_id": user_id}
    token = jwt.encode(body, "shanyrak-secret", algorithm="HS256")
    return token
    
def decode_jwt(token: str) -> int:
    data = jwt.decode(token, "shanyrak-secret", algorithms="HS256")
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
@router.post("/users/login")
def post_login(
    username: str = Form(), 
    password: str = Form(),
    db: Session = Depends(get_db)
):
    user = users_repository.get_by_email(db, username)
    
    if user.password == password:
        token = create_jwt(user.id)
        return {"access_token": token}
    
    raise HTTPException(status_code=401, detail="Invalid password")


@router.patch("/users/me")
def patch_user(
    user_data: ModifyUser, 
    token: str = Depends(oath2_scheme),
    db: Session = Depends(get_db)
):
    user_id = decode_jwt(token)
    users_repository.update_user(db, user_id, user_data)
    return Response(content="User updated", status_code=200)

@router.get("/users/me")
def get_user(token: str = Depends(oath2_scheme), db: Session = Depends(get_db)):
    user_id = decode_jwt(token)
    user = users_repository.get_by_id(db, user_id)
    user.phone = user.phone[4:].replace("-", " ")
    
    return UserReponse.model_validate(user.__dict__)


@router.post("/users/favorites/shanyraks/{id}")
def add_favorite(
    id: int,
    token: str = Depends(oath2_scheme),
    db: Session = Depends(get_db)
):
    user_id = decode_jwt(token)
    users_repository.add_favorite(db, user_id, id)
    return Response(content="Success", status_code=200)
    

@router.get("/users/favorites/shanyraks", response_model=FavoriteShanyrak)
def get_favorites(
    token: str = Depends(oath2_scheme),
    db: Session = Depends(get_db)
):
    user_id = decode_jwt(token)
    shanyraks = users_repository.get_favorite(db, user_id) 

    return {"shanyraks": shanyraks}