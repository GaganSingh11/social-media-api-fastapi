from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randint, randrange

app = FastAPI()

class Post(BaseModel):
    title:str
    body:str
    published: bool = True
    rating: Optional[int] = None

post_db = [
    {
        "title": "sunny day in yverdon",
        "body":"I am by hrose satble in yverdon",
        "id": 2
    },
    {
        "title":"Indian food provider in Yverdon",
        "body":"Now all you can eat indian for Fr19.99" ,
        "id": 3
    }
]

def find_post(id):
    for p in post_db:
        print(p["id"])
        if p["id"] == id:
            return p


@app.get("/")
def root():
    return {"message":"Hello World Gogi Singh"}

@app.get("/posts")
def get_posts():
    return {"data" : post_db}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    post_db.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/latest")
def get_latest_post():
    post = post_db[len(post_db) - 1]
    return {"latest_post" : post}

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(int(id))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id: {id} not found")
    return {"post_details" : post}

