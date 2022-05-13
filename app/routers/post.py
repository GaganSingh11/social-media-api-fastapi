from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models, schemas

router = APIRouter()

@router.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts=db.query(models.Post).all()
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()

    return posts

@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(""" INSERT INTO posts (title, body, published) VALUES (%s,%s,%s) RETURNING * """, (post.title, post.body, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict()) # ** unpacks python dict
    db.add(new_post)
    db.commit()
    db.refresh(new_post) #equal to returning * in sql

    return new_post

@router.get("/posts/latest", response_model=schemas.Post)
def get_latest_post(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts=db.query(models.Post).all()
    post = posts[len(posts) - 1]


    return post

@router.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * from posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id: {id} not found")

    return post

@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
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

@router.put("/posts/{id}", response_model=schemas.Post)
def update_post(id:int, post:schemas.PostUpdate, db: Session = Depends(get_db)):
    # cursor.execute(""" UPDATE posts SET title = %s, body = %s, published = %s WHERE id = %s""", (post.title, post.body, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_first = post_query.first()
    if post_first == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with {id} does not exist")
    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
