from sqlalchemy.orm import Session

from app.db.models import Post, Comment
from sqlite3 import IntegrityError
from app.api.serializers.posts import CreatePost, ModifyPost
from fastapi import HTTPException



class PostRepository:
    @staticmethod
    def create_post(db: Session, user_id: int, post_data: CreatePost):
        try:
            # Try to query if the user already has this post:
            existing_post = db.query(Post).filter(
                Post.user_id == user_id,
                Post.type == post_data.type,).first()

            if existing_post:
                raise HTTPException(status_code=400, detail="Post already exists")

            # If the user doesn't have this post, create it:
            post = Post(**post_data.model_dump(), user_id = user_id)
            
            db.add(post)
            db.commit()
            db.refresh(post)
            return post.id
        
        except Exception as e:
            db.rollback()
            raise e
        
    @staticmethod
    def get_post(db: Session, post_id: int):
        db_post = db.query(Post).filter(Post.id == post_id).first()
        db_comments = db.query(Comment).filter(Comment.post_id == post_id).all()
        db_comments_count = len(db_comments)
        if db_post is None:
            raise HTTPException(status_code=404, detail="Post not found")
        return db_post, db_comments_count
                
            
    @staticmethod
    def update_post(db: Session, post_id: int, user_id: int, post_data: ModifyPost):
        db_post = db.query(Post).filter(Post.id == post_id).first()
        
        if db_post is None:
            raise HTTPException(status_code=404, detail="Post not found")
        else:
            if db_post.user_id != user_id:
                raise HTTPException(status_code=403, detail="Forbidden")
            
            for key, value in post_data.model_dump(exclude_unset=True).items():
                setattr(db_post, key, value)
                
        try:
            db.commit()
            db.refresh(db_post)
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Invalid post data")
    
    
    @staticmethod
    def delete_post(db: Session, post_id: int, user_id: int):
        db_post = db.query(Post).filter(Post.id == post_id).first()
        
        if db_post is None: 
            raise HTTPException(status_code=404, detail="Post not found")
        
        if db_post.user_id != user_id:
            raise HTTPException(status_code=403, detail="Forbidden")
        
        try:
            db.delete(db_post)
            db.commit()
        except Exception as e:
            raise e
            
