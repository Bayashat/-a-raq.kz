from fastapi import APIRouter, Depends, Response

from sqlalchemy.orm import Session

from app.api.repositories.ads import AdRepository
from app.api.repositories.comments import CommentRepository
from app.api.serializers.ads import CreateAd, AdResponse, ModifyAd
from app.api.serializers.comments import AddComment, CommentResponse, CommentListResponse

from .auth import oath2_scheme, decode_jwt, get_db

router = APIRouter()
ad_repository = AdRepository()
comment_repository = CommentRepository()


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


# Comments
@router.post("/{id}/comments")
def post_comment(
    comment: AddComment,
    id: int,
    token: str = Depends(oath2_scheme),
    db: Session = Depends(get_db)
):
    user_id = decode_jwt(token)
    comment_repository.create_comment(db, user_id, id, comment)
    return Response(content="Success", status_code=200)


@router.get("/{id}/comments")
def get_comment(
    id: int,
    db: Session = Depends(get_db)
) -> CommentListResponse:
    comments = comment_repository.get_comment(db,id)
    return CommentListResponse(comments=[CommentResponse(id=c.id, content=c.content, user_id=c.user_id, ad_id=c.ad_id) for c in comments])

@router.patch("/{id}/comments/{comment_id}")
def update_comment(
    id: int,
    comment_id: int,
    comment: AddComment,
    token: str = Depends(oath2_scheme),
    db: Session = Depends(get_db)
):
    user_id = decode_jwt(token)
    comment_repository.update_comment(db,user_id, id, comment_id, comment)
    return Response(content="Comment updated", status_code=200)