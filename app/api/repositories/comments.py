from sqlalchemy.orm import Session

from app.db.models import Comment, User, Post
from app.api.serializers.comments import AddComment
from fastapi import HTTPException



class CommentRepository:
    @staticmethod
    def create_comment(db: Session, user_id: int, post_id: int, comment_data: AddComment):
        # Query User and Post
        user = db.query(User).filter(User.id == user_id).first()
        post = db.query(Post).filter(Post.id == post_id).first()
        
        if not user or not post:
            raise HTTPException(status_code=404, detail="Not found such User or Post")
        
        # Create Comment
        new_comment = Comment(
            content = comment_data.content,
            user_id = user_id,
            post_id = post_id
        )
        
        # add comment to db
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
        
    @staticmethod
    def get_comment(db: Session, post_id: int) -> list[Comment]:
        # Query Post
        post = db.query(Post).filter(Post.id == post_id).first()
        
        if not post:
            raise HTTPException(status_code=404, detail="Not found such Post")

        comments = db.query(Comment).filter(
            Comment.post_id == post_id
        ).all()
        
        return comments
        
    
    @staticmethod
    def update_comment(db: Session, user_id: int, post_id: int, comment_id: int, comment: AddComment):
        # Query User and Post
        user = db.query(User).filter(User.id == user_id).first()
        post = db.query(Post).filter(Post.id == post_id).first()
        
        if not user or not post:
            raise HTTPException(status_code=404, detail="Not found such User or Post")

        if post.user_id != user_id:
            raise HTTPException(status_code=403, detail="Forbidden")
        
        db_comment = db.query(Comment).filter(
            Comment.user_id == user_id,
            Comment.post_id == post_id,
            Comment.id == comment_id
            ).first()
        
        if db_comment is None:
            raise HTTPException(status_code=404, detail="Not found available comment for this User")
        
        db_comment.content = comment.content
        db.commit()
        db.refresh(db_comment)
        
    
    @staticmethod
    def delete_comment(db: Session, user_id: int, post_id: int, comment_id: int):
        post = db.query(Post).filter(Post.id == post_id).first()
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        if not post or not comment:
            raise HTTPException(status_code=404, detail="Not found such post or comment")
        
        if post.user_id != user_id:
            raise HTTPException(status_code=403, detail="Forbidden")
        
        db_comment = db.query(Comment).filter(
            Comment.user_id == user_id,
            Comment.post_id == post_id,
            Comment.id == comment_id
            ).first()
        
        try:
            db.delete(db_comment)
            db.commit()
        except Exception as e:
            raise e