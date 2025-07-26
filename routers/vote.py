from fastapi import  Response, Depends, HTTPException, status, APIRouter
from app import schemas,models,oauth2
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import select,delete

router = APIRouter(
    prefix="/vote",
    tags=['vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote,db: Session = Depends(get_db),
    current_user: models.user_data = Depends(oauth2.get_current_user)):
    # ✅ Step 1: Check if the post exists
    post = db.execute(select(models.Post).where(models.Post.id == vote.post_id)).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {vote.post_id} does not exist")
    # ✅ Step 2: Check if the user has already voted
    vote_query = db.execute(select(models.Vote).where(models.Vote.post_id == vote.post_id,
                                                      models.Vote.user_id == current_user.id))
    existing_vote = vote_query.first()
    # ✅ Step 3: Add vote if dir == 1
    if vote.dir == 1:
        if existing_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"User {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id=vote.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {"message": "Successfully added vote"}
    # ✅ Step 4: Remove vote if dir != 1
    else:
        if not existing_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Vote does not exist")
        db.execute(
            delete(models.Vote).where(models.Vote.post_id == vote.post_id,
                                      models.Vote.user_id == current_user.id ))
        db.commit()
        return {"message": "Successfully deleted vote"}


