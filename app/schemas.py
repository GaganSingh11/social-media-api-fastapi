from datetime import datetime
from pydantic import BaseModel, EmailStr

class PostBase(BaseModel):
    title:str
    body:str
    published: bool = True
    # rating: Optional[int] = None

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass



class Post(PostBase):
    id:int
    created_at:datetime

    class Config:
        orm_mode = True

# request in and out user model 
class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str