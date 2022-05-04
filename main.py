from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title:str
    body:str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
def root():
    return {"message":"Hello World Gogi Singh"}

@app.get("/posts")
def get_posts():
    return {"data" : "This is your post"}

@app.post("/createpost")
def create_post(post: Post):
    print(post)
    return {"data": post}