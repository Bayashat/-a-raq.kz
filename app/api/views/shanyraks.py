from fastapi import APIRouter, Depends, Response

from sqlalchemy.orm import Session

from app.api.repositories.posts import PostRepository
from app.api.repositories.comments import CommentRepository
from app.api.serializers.posts import CreatePost, PostResponse, ModifyPost, SearchResultResponse, SearchResponse
from app.api.serializers.comments import AddComment, CommentResponse, CommentListResponse

from .auth import oath2_scheme, decode_jwt, get_db

router = APIRouter()
post_repository = PostRepository()
comment_repository = CommentRepository()


@router.post("/")
def post_post(
    post: CreatePost,
    token: str = Depends(oath2_scheme),
    db: Session = Depends(get_db)
):
    user_id = decode_jwt(token)
    post_id = post_repository.create_post(db, user_id, post)
    return {"id": str(post_id)}
    

@router.get("/{id}")
def get_post(
    id: int,
    db: Session = Depends(get_db)
) -> PostResponse:
    db_post, db_comments_count = post_repository.get_post(db, id)

    response = PostResponse(
        id = db_post.id,
        type = db_post.type,
        price = db_post.price,
        address = db_post.address,
        area = db_post.area,
        rooms_count = db_post.rooms_count,
        description = db_post.description,
        user_id = db_post.user_id,
        total_comments = db_comments_count
    )
    
    return response


@router.patch("/{id}")
def update_post(
    id: int,
    post_data: ModifyPost,
    token: str = Depends(oath2_scheme),
    db: Session = Depends(get_db)
):
    user_id = int(decode_jwt(token))
    post_repository.update_post(db, id, user_id, post_data)
    return Response(content="Post updated", status_code=200)


@router.delete("/{id}")
def delete_post(
    id: int,
    token: str = Depends(oath2_scheme),
    db: Session = Depends(get_db)
):
    user_id = decode_jwt(token)
    post_repository.delete_post(db, id, user_id)
    return Response(content=f"Post with id {user_id} deleted")


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
    return CommentListResponse(comments=[CommentResponse(id=c.id, content=c.content, user_id=c.user_id, ad_id=c.post_id) for c in comments])

@router.patch("/{id}/comments/{comment_id}")
def update_comment(
    id: int,
    comment_id: int,
    comment: AddComment,
    token: str = Depends(oath2_scheme),
    db: Session = Depends(get_db)
):
    user_id = decode_jwt(token)
    comment_repository.update_comment(db, user_id, id, comment_id, comment)
    return Response(content="Comment updated", status_code=200)


@router.delete("/{id}/comments/{comment_id}")
def delete_comment(
    id: int,
    comment_id: int,
    token: str = Depends(oath2_scheme),
    db: Session = Depends(get_db)
):
    user_id = decode_jwt(token)
    comment_repository.delete_comment(db, user_id, id, comment_id)
    return Response(content="Comment deleted", status_code=200)


@router.get("/", response_model=SearchResultResponse)
def get_posts(
    db: Session = Depends(get_db),
    limit: int = 10,
    offset: int = 0,
    type: str = "rent",
    rooms_count: int = 2,
    price_from: int = 0,
    price_until: int = 300000
):
    posts = post_repository.get_posts(db, limit, offset, type, rooms_count, price_from, price_until)
    return SearchResultResponse(total=len(posts), objects=[SearchResponse.model_validate(post.__dict__) for post in posts])