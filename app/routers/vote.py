from fastapi import Response, status, HTTPException, Depends, APIRouter
from pydantic import model_serializer
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..database import get_db
from .. import models, schemas, oauth2

router = APIRouter(
    prefix='/vote',
    tags=['Vote']
)

@router.post("", status_code=status.HTTP_201_CREATED)
async def submit_vote(vote: schemas.VoteSubmitSchema, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    # database query happens here
    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id)
    found_vote = vote_query.first() #result of the vote_query

    # if vote direction is equal to 1 or True
    if vote.direction:
        # check if an there is already an existing vote
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        
        # if the vote does not exist, create the vote and commit to the db
        new_vote = models.Votes(user_id = current_user.id, post_id = vote.post_id)
        db.add(new_vote)

        try:
            db.commit()
            return {"message": "vote succesfully created"}
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"post with id {vote.post_id} does not exist")

    # if vote direction is equal to 0 or False
    else:
        if found_vote == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='vote does not exist')
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "vote succesfully deleted"}