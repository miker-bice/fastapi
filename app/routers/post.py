from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func, desc, true
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from typing import List, Optional, Dict

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

# default values for endpoint query parameters - ALWAYS CHANGE HERE
DEFAULT_RESPONSE_LIMIT = 10
DEFAULT_SKIP_LIMIT = 0


# @router.get("", response_model=List[schemas.PostResponse])
@router.get("", response_model=List[schemas.PostOutVotesSchema])
async def get_posts(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = DEFAULT_RESPONSE_LIMIT, offset:int = DEFAULT_SKIP_LIMIT, search: Optional[str] = ""):
    query = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id)

    new_results = query.filter(models.Post.title.contains(search)).limit(limit).offset(offset).all()

    return new_results


@router.get("/{post_id}", response_model=schemas.PostOutVotesSchema)
async def get_post(post_id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")

    return post


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id = current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    deleted_post = db.query(models.Post).filter(models.Post.id == post_id)
    post = deleted_post.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    # db.delete(deleted_post)
    deleted_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{post_id}", response_model=schemas.PostResponse)
def update_post(post_id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    updated_post = post_query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()

