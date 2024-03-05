from sqlalchemy.orm import Session

from app.db.models import Comment, User, Ad
from app.api.serializers.comments import AddComment
from fastapi import HTTPException



class CommentRepository:
    @staticmethod
    def create_comment(db: Session, user_id: int, ad_id: int, comment_data: AddComment):
        # Query User and Ad
        user = db.query(User).filter(User.id == user_id).first()
        ad = db.query(Ad).filter(Ad.id == ad_id).first()
        
        if not user or not ad:
            raise HTTPException(status_code=404, detail="Not found such User or Ad")
        # Create Comment
        new_comment = Comment(
            content = comment_data.content,
            user_id = user_id,
            ad_id = ad_id
        )
        
        # add comment to db
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
        
    @staticmethod
    def get_comment(db: Session, ad_id: int) -> list[Comment]:
        # Query Ad
        ad = db.query(Ad).filter(Ad.id == ad_id).first()
        
        if not ad:
            raise HTTPException(status_code=404, detail="Not found such User or Ad")

        comments = db.query(Comment).filter(
            Comment.ad_id == ad_id
        ).all()
        
        return comments
        
    
    @staticmethod
    def update_comment(db: Session, user_id: int, ad_id: int, comment_id: int, comment: AddComment):
        # Query User and Ad
        user = db.query(User).filter(User.id == user_id).first()
        ad = db.query(Ad).filter(Ad.id == ad_id).first()
        
        if not user or not ad:
            raise HTTPException(status_code=404, detail="Not found such User or Ad")

        db_comment = db.query(Comment).filter(
            Comment.user_id == user_id,
            Comment.ad_id == ad_id,
            Comment.id == comment_id
            ).first()
        
        if db_comment is None:
            raise HTTPException(status_code=404, detail="Not found available comment for this User")
        
        db_comment.content = comment.content
        db.commit()
        db.refresh(db_comment)