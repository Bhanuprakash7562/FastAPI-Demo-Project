from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Relationship
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()


class Blog(base):
    __tablename__ = "blogDetails"
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    date = Column(DateTime(timezone=False),nullable=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    
    creator = Relationship("Users", back_populates="blogs")

class Users(base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    
    blogs = Relationship("Blog", back_populates="creator")