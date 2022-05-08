from tokenize import String
from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, text
from .database import Base


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False )
    title = Column(String, nullable=False )
    body = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default= text('now()') )