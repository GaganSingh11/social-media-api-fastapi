from tokenize import String
from sqlalchemy import Column, Integer, String, Boolean
from .database import Base


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False )
    title = Column(String, nullable=False )
    body = Column(String, nullable=False)
    published = Column(Boolean, default= True)