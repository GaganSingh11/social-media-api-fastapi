from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth
from .config import setting

models.Base.metadata.create_all(bind = engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message":"Welcome to Social Media API. Please follow the Documentation yo get started"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)