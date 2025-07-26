# app.oath2.py
from jose import JWTError,jwt
from app import models
from app.schemas import TokenData

from sqlalchemy import select
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime,timedelta
from fastapi import Depends,HTTPException,status
from .config import settings



oath2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# SECRET_KEY
# ALGORITHM
# EXPERIATION_TIME

SECRET_KEY =settings.secret_key
ALGORITHM =settings.algorithm
ACCESS_TOKEN_EXPIRE_TIME = settings.access_token_expires_minutes

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)
    to_encode.update({"exp": expire})
    jwt_token = jwt.encode (to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return jwt_token
    

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        return TokenData(id=str(user_id))  # Ensure string output
    except JWTError:
        raise credentials_exception


    
     
    
# # Updated get_current_user to use user_data
def get_current_user(token: str = Depends(oath2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    token_data = verify_access_token(token, credentials_exception)
    user_id = token_data.id  # Extract actual ID
    # Get user ID from token (string)    
    # Fetch user from database using user_data model
    user = db.execute(select(models.user_data).where(models.user_data.id == user_id)).scalar_one_or_none() 
    if not user:
        raise credentials_exception
        
    return user




