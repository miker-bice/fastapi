from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

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
async def get_posts():
    cursor.execute("""SELECT * FROM posts;""")
    results = cursor.fetchall()
    return {"data": results}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: PostSchema):
    cursor.execute("""INSERT INTO posts (title, content, is_published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.is_published))
    new_post = cursor.fetchone()
    connection.commit()
    
    return {"data": new_post}