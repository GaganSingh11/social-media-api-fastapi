from typing import Optional
from fastapi import Body, FastAPI
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
        "body":"I am by hrose satble in yverdon"
    },
    {
        "title":"Indian food provider in Yverdon",
        "body":"Now all you can eat indian for Fr19.99" 
    }
]


@app.get("/")
def root():
    return {"message":"Hello World Gogi Singh"}

@app.get("/posts")
def get_posts():
    return {"data" : post_db}

@app.post("/posts")
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    post_db.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post(id):
    print(id)
    return {"post_details" : f"Here is the post for {id}"}