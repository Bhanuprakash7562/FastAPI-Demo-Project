from fastapi import APIRouter, Depends, HTTPException, status
from .. import database, schemas, models
from passlib.context import CryptContext


router = APIRouter(prefix="/users",tags=["USERS"])

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

@router.post("/create-user")
def create_user(request : schemas.Users, db : database.Session = Depends(database.get_db)):
    hashed_pwd = pwd_context.hash(request.password)
    q = database.text('insert into public."Users" (name, email, password) values (:name, :email, :password)')
    vals = db.execute(q, {"name": request.name, "email": request.email, "password": hashed_pwd})
    db.commit()
    return {"Response": f"{vals.rowcount} rows inserted."}

@router.get("/get-user/{email}")
def get_user(email, db : database.Session = Depends(database.get_db)):
    q = database.text('select * from public."Users" where email = :email')
    result = db.execute(q, {"email": email}).first()
    return {"data":list(result)[0:-1]}