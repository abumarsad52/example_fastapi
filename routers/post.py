#routers/post.py
from fastapi import  Response, Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import select, delete, update,func
from typing import List,Optional
from app import oauth2
from app import schemas
from app import models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/posts",        # optional
    tags=["Posts"]          # ✅ FIX: wrap the string in a list
)

# Get all posts

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),current_user: models.user_data = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ""):
    # 🧠 Step 1: Filter Posts by owner and title
    stmt = (
        select(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .where(models.Post.owner_id == current_user.id,models.Post.title.ilike(f"%{search}%"))
        .group_by(models.Post.id)
        .limit(limit)
        .offset(skip))
    # 🧠 Step 2: Execute upgraded 2.0 style query
    results = db.execute(stmt).all()
    return results




    
    

# Get post by ID
@router.get("/{id}", response_model=schemas.PostOut)
def get_post_by_id(id: int,db: Session = Depends(get_db),
    current_user: models.user_data = Depends(oauth2.get_current_user)):
    stmt = (
        select(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .where(models.Post.id == id,models.Post.owner_id == current_user.id)
        .group_by(models.Post.id))
    post = db.execute(stmt).first()
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    return post






# Create a new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(
    post_data: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.user_data = Depends(oauth2.get_current_user)  # Expects User model, not int
):
    # Associate the post with the current user
    new_post = models.Post(owner_id=current_user.id,**post_data.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post





#Delete post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: models.user_data = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post")
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)







# Update an existing post

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.PostResponse)
def update_post(id: int, post_data: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.user_data = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this post")

    post_query.update(post_data.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
