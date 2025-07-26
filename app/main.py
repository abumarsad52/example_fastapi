# app/main.py

from fastapi import FastAPI
from . import models
from .database import engine
from routers import post, user,auth,vote # 👈 import your routers here
from app.config import settings
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)


# print(f"databse_name: {settings.database_name}")


@app.get("/")
def root():
    return {"message": "Welcome to my custom API!"}

# 👇 include routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)