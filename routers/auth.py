#routers/auth.py
from fastapi import Depends, HTTPException, status, APIRouter,Response
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app import models, oauth2, utils
from sqlalchemy import select
router = APIRouter(
    tags=["Authentication"],  # ✅ FIX: wrap the string in a list
)


# login user

@router.post("/login")
def login_in(user_credentials:OAuth2PasswordRequestForm=Depends(),db:Session = Depends(get_db)):
    user = select(models.user_data).where(models.user_data.email == user_credentials.username)
    user_logs = db.execute(user).scalar_one_or_none()
    if not user_logs:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )
    if not utils.verify(user_credentials.password, user_logs.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )
    # Create a token for the user
    access_token = oauth2.create_access_token(data={"user_id": str(user_logs.id)})
    return {"access_token": access_token, "token_type": "bearer"}  




