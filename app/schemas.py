from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# FOR POST
class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = True

class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# FOR USER
class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=50)

class UserCreateResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


# FOR AUTHENTICATION
class LoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=50)

class TokenSchema(BaseModel):
    access_token: str
    token_type: str

class TokenDataSchema(BaseModel):
    id: str