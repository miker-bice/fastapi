from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils

router = APIRouter(tags=["Authentication"])

@router.post('/login')
async def login(user_credentials: schemas.LoginSchema, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid credentials")

    is_password_valid = utils.verify(user_credentials.password, user.password)

    if not is_password_valid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid credentials")

    return Response(status_code=status.HTTP_200_OK)