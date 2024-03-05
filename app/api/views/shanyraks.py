from fastapi import APIRouter, Depends, Response

from sqlalchemy.orm import Session

from app.api.repositories.ads import AdRepository
from app.api.serializers.ads import CreateAd, AdResponse, ModifyAd
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
    db: Session = Depends(get_db)
):
    db_ad = ad_repository.get_ad(db, id)

    return AdResponse.model_validate(db_ad.__dict__)


@router.patch("/{id}")
def update_ad(
    id: int,
    ad_data: ModifyAd,
    db: Session = Depends(get_db)
):
    ad_repository.update_ad(db, id, ad_data)
    return Response(content="Ad updated", status_code=200)


@router.delete("/{id}")
def delete_ad(
    id: int,
    token: str = Depends(oath2_scheme),
    db: Session = Depends(get_db)
):
    user_id = decode_jwt(token)
    ad_repository.delete_ad(db, id, user_id)
    return Response(content=f"Ad with id {user_id} deleted")