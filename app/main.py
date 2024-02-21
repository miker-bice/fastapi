import time
import psycopg2
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency


class PostSchema(BaseModel):
    title: str
    content: str
    is_published: bool

# DB connection
while True:
    try:
        connection = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='password', cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        print("Database connection successfull")
        break
    except Exception as error:
        print(f"Error! {error}")
        time.sleep(3)


@app.get("/")
async def root():
    return {"message": "Hello this is HOMIEZZ!"}


@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()

    return {"data": posts}


@app.get("/posts/{post_id}")
async def get_post(post_id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(post_id)))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")

    return {"data": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: PostSchema, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, is_published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.is_published))
    # new_post = cursor.fetchone()
    # connection.commit()

    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data": new_post}


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""", (str(post_id)))
    # deleted_post = cursor.fetchone()
    # connection.commit()
    deleted_post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    
    db.delete(deleted_post)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}")
def update_post(post_id: int, post: PostSchema, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title=%s, content=%s, is_published=%s WHERE id=%s RETURNING *""", (post.title, post.content, post.is_published, str(post_id)))
    # updated_post = cursor.fetchone()

    # connection.commit()
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    updated_post = post_query.first()
    
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return {"data": post_query.first()}
