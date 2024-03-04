from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.api.repositories.ads import AdRepository
from app.api.serializers.ads import CreateAd, AdResponse
from .auth import oath2_scheme, decode_jwt, get_db

router = APIRouter()
ad_repository = AdRepository()


@router.post("/")
def post_ad(
    ad: CreateAd,
    token: str = Depends(oath2_scheme),
    db: Session = Depends(get_db)
):
    user_id = decode_jwt(token)
    ad_id = ad_repository.create_ad(db, user_id, ad)
    return {"id": str(ad_id)}
    

@router.get("/{id}")
def get_ad(
    id: int,
    token: str = Depends(oath2_scheme),
    db: Session = Depends(get_db)
):
    user_id = decode_jwt(token)
    db_ad = ad_repository.get_ad(db, user_id)

    return AdResponse.model_validate(db_ad.__dict__)