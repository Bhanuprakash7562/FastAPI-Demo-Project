from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from database import engine, session, Session, get_db
import schemas

app = FastAPI()

schemas.base.metadata.create_all(bind=engine)


class Blogdata(BaseModel):
    title : str
    body : str
    published_at : Optional[datetime] = None
    
    class config:
        orm_mode = True

@app.post("/create-blog")
def create(request : Blogdata, db : Session = Depends(get_db)):
    newblog = schemas.Blog(title=request.title, body=request.body, date=request.published_at or datetime.utcnow())
    db.add(newblog)
    db.commit()
    db.refresh(newblog)
    return newblog