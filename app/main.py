from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

from . import credentials

models.Base.metadata.create_all(bind = engine)

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

@app.get('/sqlalchemy')
def test_posts(db: Session = Depends(get_db)):
    posts=db.query(models.Post).all()
    return {"data": posts}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts=db.query(models.Post).all()
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()

    return {"data" : posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    # cursor.execute(""" INSERT INTO posts (title, body, published) VALUES (%s,%s,%s) RETURNING * """, (post.title, post.body, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict()) # ** unpacks python dict
    db.add(new_post)
    db.commit()
    db.refresh(new_post) #equal to returning * in sql

    return {"data": new_post}

@app.get("/posts/latest")
def get_latest_post(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts=db.query(models.Post).all()
    post = posts[len(posts) - 1]


    return {"latest_post" : post}

@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * from posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id: {id} not found")

    return {"post_details" : post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    
    # cursor.execute(""" DELETE FROM posts WHERE id = %s returning * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with {id} does not exist")
    
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int, post:Post, db: Session = Depends(get_db)):
    # cursor.execute(""" UPDATE posts SET title = %s, body = %s, published = %s WHERE id = %s""", (post.title, post.body, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_first = post_query.first()
    if post_first == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with {id} does not exist")
    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return {"data": post_query.first()}
