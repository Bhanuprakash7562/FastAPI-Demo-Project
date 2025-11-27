from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from .. import schemas, database, models, token
from .user import pwd_context
from datetime import timedelta


router = APIRouter(tags=["LOGIN"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/login", response_model=schemas.TokenResponse)
def login(request : OAuth2PasswordRequestForm = Depends(), db : database.Session = Depends(database.get_db)):
    user = db.query(models.Users).filter(models.Users.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    if not pwd_context.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    access_token_expires = timedelta(minutes=token.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token.create_token(subject=user.email, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(atoken : str = Depends(oauth2_scheme), db : database.Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token_data = token.decode_token(atoken)
        username = token_data.sub
        if username is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    
    user = db.query(models.Users).filter(models.Users.email == username).first()
    if user is None:
        raise credentials_exception
    return user