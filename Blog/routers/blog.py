from fastapi import APIRouter, Depends, HTTPException, status
from .. import database, schemas, models
from . import login
from datetime import datetime

router = APIRouter(prefix="/blogs", tags=["BLOGS"])

@router.get("/get-Blogs")
def get_data(db : database.Session = Depends(database.get_db), current_user : models.Users = Depends(login.get_current_user)):
    q = database.text('select * from public."blogDetails" order by id')
    rows = db.execute(q).all()
    return [dict(row._mapping) for row in rows]

@router.post("/create-blog")
def create(request : schemas.Blogdata, db : database.Session = Depends(database.get_db)):
    newblog = models.Blog(title=request.title, body=request.body, date=request.published_at or datetime.utcnow(), user_id=request.used_id)
    user = db.query(models.Users).filter(models.Users.id == request.used_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found. Please cross check the user-id.")
    db.add(newblog)
    db.commit()
    db.refresh(newblog)
    return newblog

@router.get("/get-Blogdata/{id}")
def get_data(id, db : database.Session = Depends(database.get_db)):
    q = database.text('select * from public."blogDetails" where id = :id order by id')
    rows = db.execute(q, {"id": id}).all() # returns list of tuples
    print(rows)
    if not rows:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Records not found on that {id}.")
    return [dict(row._mapping) for row in rows]

@router.put("/update-data/{id}")
def update_data(id, request : schemas.Blogdata, db : database.Session = Depends(database.get_db)):
    q = database.text('update public."blogDetails" set title = :title, body = :body, "date" = :date where id = :id')
    result = db.execute(q, {"title": request.title, "body":request.body, "date": request.published_at or datetime.utcnow(), "id" : id})
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"No rows found on the id : {id}")
    return {"Response": f"Updated {result.rowcount} rows."}

@router.delete("/delete-blog/{id}")
def delete_blog(id, db : database.Session = Depends(database.get_db)):
    q = database.text('delete from public."blogDetails" where id = :id')
    result = db.execute(q, {"id": id})
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"{id} not found.")
    return {"Response": f"Blog {id} is deleted."}