from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class PostSchema(BaseModel):
    title: str
    content: str
    rating: Optional[int] = None


@app.get("/")
async def root():
    return {"message": "Hello this is homiezzzz!"}


@app.post("/create_post")
async def create_post(request: PostSchema):
    print(request.rating)
    
    return request