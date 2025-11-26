from fastapi import FastAPI, Depends, HTTPException, status
from datetime import datetime
from . import database, schemas, models
from passlib.context import CryptContext
from .routers import blog, user, login

app = FastAPI()

models.base.metadata.create_all(bind=database.engine) # This Line will create tables in database immediately after defining in models.py

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(login.router)

# --------------------------------------Commented endpoints in main.py and moved to routers folder----------------------------------------------------

# pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


# @app.post("/create-blog", tags=["Blogs"])
# def create(request : schemas.Blogdata, db : database.Session = Depends(database.get_db)):
#     newblog = models.Blog(title=request.title, body=request.body, date=request.published_at or datetime.utcnow(), user_id=request.used_id)
#     user = db.query(models.Users).filter(models.Users.id == request.used_id).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found. Please cross check the user-id.")
#     db.add(newblog)
#     db.commit()
#     db.refresh(newblog)
#     return newblog

# @app.get("/get-Blogs", tags=["Blogs"])
# def get_data(db : database.Session = Depends(database.get_db)):
#     q = database.text('select * from public."blogDetails" order by id')
#     rows = db.execute(q).all()
#     return [dict(row._mapping) for row in rows]

# @app.get("/get-Blogdata/{id}", tags=["Blogs"])
# def get_data(id, db : database.Session = Depends(database.get_db)):
#     q = database.text('select * from public."blogDetails" where id = :id order by id')
#     rows = db.execute(q, {"id": id}).all() # returns list of tuples
#     print(rows)
#     if not rows:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Records not found on that {id}.")
#     return [dict(row._mapping) for row in rows]

# @app.put("/update-data/{id}", tags=["Blogs"])
# def update_data(id, request : schemas.Blogdata, db : database.Session = Depends(database.get_db)):
#     q = database.text('update public."blogDetails" set title = :title, body = :body, "date" = :date where id = :id')
#     result = db.execute(q, {"title": request.title, "body":request.body, "date": request.published_at or datetime.utcnow(), "id" : id})
#     db.commit()
#     if result.rowcount == 0:
#         raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"No rows found on the id : {id}")
#     return {"Response": f"Updated {result.rowcount} rows."}

# @app.delete("/delete-blog/{id}", tags=["Blogs"])
# def delete_blog(id, db : database.Session = Depends(database.get_db)):
#     q = database.text('delete from public."blogDetails" where id = :id')
#     result = db.execute(q, {"id": id})
#     db.commit()
#     if result.rowcount == 0:
#         raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"{id} not found.")
#     return {"Response": f"Blog {id} is deleted."}

# @app.post("/create-user", tags=["Users"])
# def create_user(request : schemas.Users, db : database.Session = Depends(database.get_db)):
#     hashed_pwd = pwd_context.hash(request.password)
#     q = database.text('insert into public."Users" (name, email, password) values (:name, :email, :password)')
#     vals = db.execute(q, {"name": request.name, "email": request.email, "password": hashed_pwd})
#     db.commit()
#     return {"Response": f"{vals.rowcount} rows inserted."}

# @app.get("/get-user/{email}", tags=["Users"])
# def get_user(email, db : database.Session = Depends(database.get_db)):
#     q = database.text('select * from public."Users" where email = :email')
#     result = db.execute(q, {"email": email}).first()
#     return {"data":list(result)[0:-1]}


# @app.post("/verify-user")
# def verify_user(request : schemas.Login, db : database.Session = Depends(database.get_db)):
#     q = database.text('select * from public."Users" where email = :email')
#     result = db.execute(q, {"email": request.email}).all()
#     if len(result) == 0:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="row not found")
#     print(result)
#     return [dict(row._mapping) for row in result]