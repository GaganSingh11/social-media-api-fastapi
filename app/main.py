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
    

@app.get("/")
def root():
    return {"message":"Hello World Gogi Singh"}

@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()

    return {"data" : posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(""" INSERT INTO posts (title, body, published) VALUES (%s,%s,%s) RETURNING * """, (post.title, post.body, post.published))
    new_post = cursor.fetchone()
    conn.commit()

    return {"data": new_post}

@app.get("/posts/latest")
def get_latest_post():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    post = posts[len(posts) - 1]

    return {"latest_post" : post}

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute(""" SELECT * from posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id: {id} not found")

    return {"post_details" : post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    
    cursor.execute(""" DELETE FROM posts WHERE id = %s returning * """, (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with {id} does not exist")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    cursor.execute(""" UPDATE posts SET title = %s, body = %s, published = %s WHERE id = %s""", (post.title, post.body, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with {id} does not exist")

    return {"data": updated_post}
