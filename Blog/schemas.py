from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Blogdata(BaseModel):
    title : str
    body : str
    published_at : Optional[datetime] = None
    used_id : int
    
    class config:
        orm_mode = True


class Users(BaseModel):
    name : str
    email : str
    password : str

class login(BaseModel):
    username : str
    password : str
    
    class config:
        orm_mode = True