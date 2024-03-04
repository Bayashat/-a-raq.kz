from sqlalchemy.orm import Session

from app.db.models import Ad
from sqlite3 import IntegrityError
from app.api.serializers.ads import CreateAd, ModifyAd
from fastapi import HTTPException



class AdRepository:
    @staticmethod
    def create_ad(db: Session, user_id: int, ad_data: CreateAd):
        try:
            # Try to query if the user already has this ad:
            existing_ad = db.query(Ad).filter(
                Ad.user_id == user_id,
                Ad.type == ad_data.type,).first()

            if existing_ad:
                raise HTTPException(status_code=400, detail="Ad already exists")

            # If the user doesn't have this ad, create it:
            ad = Ad(**ad_data.model_dump(), user_id = user_id)
            
            db.add(ad)
            db.commit()
            db.refresh(ad)
            return ad.id
        except Exception as e:
            # Handle exceptions (e.g., database errors, custom exceptions)
            db.rollback()
            raise e
        
    @staticmethod
    def get_ad(db: Session, ad_id: int):
        try:
            # try to query if the ad exist
            db_ad = db.query(Ad).filter(Ad.id == ad_id).first()
            return db_ad
        except Exception as e:
            db.rollback()
            raise e
                
            
    @staticmethod
    def update_ad(db: Session, ad_id: int, ad_data: ModifyAd):
        db_ad = db.query(Ad).filter(Ad.id == ad_id).first()
        
        if db_ad is None:
            raise HTTPException(status_code=404, detail="Ad not found")
        else:
            for key, value in ad_data.model_dump(exclude_unset=True).items():
                setattr(db_ad, key, value)
                
        try:
            db.commit()
            db.refresh(db_ad)
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Invalid ad data")