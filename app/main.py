from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from . import credentials

app = FastAPI()

class Post(BaseModel):
    title:str
    body:str
    published: bool = True
    # rating: Optional[int] = None

while True:

    try:
        conn = psycopg2.connect(
            host = credentials.hostname,
            dbname= credentials.database, 
            port = credentials.port,
            user= credentials.user, 
            password= credentials.password,
            cursor_factory=RealDictCursor
            )
        cursor = conn.cursor()
        print ("Database connection was successful")
        break
    except Exception as error:
        print(f'Connection to database failed. Error:{error}')
        time.sleep(2)
    


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

def find_index_post(id):
    for i,p in enumerate(post_db):
        if p['id'] == id:
            return i



# @app.get("/")
# def root():
#     return {"message":"Hello World Gogi Singh"}

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

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    #delete post
    # find the index in array that has required id
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with {id} does not exist")
    post_db.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with {id} does not exist")

    post_dict = post.dict()
    post_dict['id'] = id
    post_db[index] = post_dict
    return {"data":post_dict}
