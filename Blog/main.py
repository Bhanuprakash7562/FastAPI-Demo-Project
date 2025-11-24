from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from database import engine, Session, get_db, text
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

@app.get("/get-blogdata")
def get_data(db : Session = Depends(get_db)):
    q = text('select * from public."blogDetails" order by id')
    rows = db.execute(q).all()
    return [dict(row._mapping) for row in rows]