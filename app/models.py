# app.model.py
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,relationship
from sqlalchemy import Integer, String, Boolean, TIMESTAMP, text,ForeignKey
from datetime import datetime
from typing import List 
class Base(DeclarativeBase):
    pass

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    published: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default='True')
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True),nullable=False,server_default=text('NOW()'))
    owner_id: Mapped[int] = mapped_column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    #  Define relationship to parent
    owner: Mapped["user_data"] = relationship("user_data", back_populates="posts")
    
    
    
    
    
class user_data(Base):
    __tablename__ ="users"
    id:Mapped[int] = mapped_column(Integer,primary_key=True,nullable=False)
    email:Mapped[str] = mapped_column(String,nullable=False, unique=True)
    password:Mapped[str]= mapped_column(String,nullable= False)
    created_at: Mapped[datetime] = mapped_column(
    TIMESTAMP(timezone=True),
    nullable=False,
    server_default=text("now()"))
    #  Define relationship to child
    posts: Mapped[List["Post"]] = relationship("Post", back_populates="owner", cascade="all, delete")



class Vote(Base):
    __tablename__="votes"
    user_id: Mapped[int]=mapped_column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    post_id: Mapped[int]=mapped_column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)