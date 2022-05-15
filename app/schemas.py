from datetime import datetime
from pydantic import BaseModel, EmailStr, conint
from typing import Optional

class PostBase(BaseModel):
    title:str
    body:str
    published: bool = True
    # rating: Optional[int] = None

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass


class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True

class Post(PostBase):
    id:int
    created_at:datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True

# request in and out user model 
class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

