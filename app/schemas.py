# app.schemas.py

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from pydantic.types import Annotated


# -----------------------------
# Schema for User Registration
# -----------------------------
class UserCreate(BaseModel):
    email: EmailStr         # User's email (validated format)
    password: str           # User's password (plaintext input)

# -----------------------------
# Schema for User Output (response after creation/login etc.)
# -----------------------------
class User_out(BaseModel):
    id: int                 # User's unique ID
    email: EmailStr         # User's email
    created_at: datetime    # Timestamp of user creation

    class Config:
        from_attributes = True  # Tells Pydantic to load from ORM model attributes

# -----------------------------
# Base schema for creating/updating posts
# -----------------------------
class PostBase(BaseModel):
    title: str              # Title of the post
    content: str            # Main content/body of the post
    published: bool = True  # Optional: whether the post is published or not (default: True)

# -----------------------------
# Schema for Creating a Post (inherits from PostBase)
# -----------------------------
class PostCreate(PostBase):
    pass                    # Inherits everything from PostBase

# -----------------------------
# Schema for Returning Post Data (includes owner info)
# -----------------------------
class PostResponse(PostBase):
    id: int                 # Post ID
    created_at: datetime    # Timestamp of post creation
    owner_id: int           # ID of the user who created the post
    owner: User_out         # Full user info of the post's owner (nested response)

    class Config:
        from_attributes = True  # Enables ORM mode for SQLAlchemy

# -----------------------------
# Schema for User Login
# -----------------------------
class UserLogin(BaseModel):
    email: EmailStr         # Email entered at login
    password: str           # Password entered at login

# -----------------------------
# Schema for Access Token Response
# -----------------------------
class Token(BaseModel):
    access_token: str       # JWT token string
    token_type: str         # Type of token (usually 'bearer')

# -----------------------------
# Schema for Extracted Data from Token (used internally)
# -----------------------------
class TokenData(BaseModel):
    id: Optional[str] = None  # User ID extracted from token payload

# -----------------------------
# Schema for Voting on Posts
# -----------------------------
class Vote(BaseModel):
    post_id: int                                # ID of the post being voted on
    dir: Annotated[int, Field(le=1)]            # 0 = remove vote, 1 = add vote (must be ≤ 1)

    # 💡 You can also do: dir: Annotated[int, Field(ge=0, le=1)] to restrict between 0 and 1



# Wrapper schema for a post with vote count
class PostOut(BaseModel):
    Post: PostResponse      # The full post response (including owner)
    votes: int              # Number of votes (likes)

    class Config:
        from_attributes = True