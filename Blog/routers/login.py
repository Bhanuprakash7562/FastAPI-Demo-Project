from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, database, models
from .user import pwd_context


router = APIRouter(tags=["LOGIN"])


@router.post("/login")
def login(request : schemas.login, db : database.Session = Depends(database.get_db)):
    user = db.query(models.Users).filter(models.Users.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    if not pwd_context.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    return user