# routers/user.py
from fastapi import  Depends, HTTPException, status,APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from app import models, schemas,utils
from app.database import get_db

router = APIRouter(
    prefix="/user",        # optional
    tags=["Users"]          # ✅ FIX: wrap the string in a list
)

# create user data
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User_out)
def create_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user_data.password)
    user_data.password = hashed_password
    new_user = models.user_data(**user_data.dict())
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="This email already exists.")

        

@router.get("/{id}",response_model=schemas.User_out)
def get_user_id(id:int,db:Session = Depends(get_db)):
    tmt = select(models.user_data).where(models.user_data.id == id)
    post = db.execute(tmt).scalar_one_or_none()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The post with id {id} not found"
        )
    return post