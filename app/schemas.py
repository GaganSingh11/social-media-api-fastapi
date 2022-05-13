from pydantic import BaseModel

class Post(BaseModel):
    title:str
    body:str
    published: bool = True
    # rating: Optional[int] = None

class PostCreate(BaseModel):
    pass

class PostUpdate(BaseModel):
    pass
