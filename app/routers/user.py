from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from sqlalchemy.exc import IntegrityError

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreateResponse)
async def create_user(user: schemas.UserCreateSchema, db: Session = Depends(get_db)):
    # password hashing
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    try:
        db.commit()
    # Raise this error if the email given is already used
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{user.email} is already taken")

    db.refresh(new_user)

    return new_user 


@router.get("/{user_id}", response_model=schemas.UserCreateResponse)
async def get_user(user_id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user {user_id} not found')

    return user