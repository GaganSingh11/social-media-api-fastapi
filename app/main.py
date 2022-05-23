from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import setting

from fastapi.middleware.cors import CORSMiddleware


# models.Base.metadata.create_all(bind = engine)

app = FastAPI()

origins = ["*"] # list of domain that are allowed to talk with this api

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    # return {"message":"Welcome to social media API. Please follow the documentation to get started. You may access documentation at /docs"}
    return {"message":"Deployed using CI/CD pipeline"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)