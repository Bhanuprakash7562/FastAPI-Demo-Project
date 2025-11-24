from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()


class Blog(base):
    __tablename__ = "blogDetails"
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    date = Column(DateTime(timezone=False),nullable=True)