from fastapi import FastAPI, Depends, HTTPException, status
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

@app.get("/get-blogdata/{id}")
def get_data(id, db : Session = Depends(get_db)):
    q = text('select * from public."blogDetails" where id = :id order by id')
    rows = db.execute(q, {"id": id}).all() # returns list of tuples
    print(rows)
    if not rows:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Records not found on that {id}.")
    # return [{"id":row[0], "Title":row[1], "Body":row[2], "Published_at":row[3]} for row in rows]
    return [dict(row._mapping) for row in rows]

@app.put("/update-data/{id}")
def update_data(id, request : Blogdata, db : Session = Depends(get_db)):
    q = text('update public."blogDetails" set title = :title, body = :body, "date" = :date where id = :id')
    result = db.execute(q, {"title": request.title, "body":request.body, "date": request.published_at or datetime.utcnow(), "id" : id})
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"No rows found on the id : {id}")
    return {"Response": f"Updated {result.rowcount} rows."}

@app.delete("/delete-blog/{id}")
def delete_blog(id, db : Session = Depends(get_db)):
    q = text('delete from public."blogDetails" where id = :id')
    result = db.execute(q, {"id": id})
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"{id} not found.")
    return {"Response": f"Blog {id} is deleted."}