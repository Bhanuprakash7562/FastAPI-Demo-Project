from . import schemas
from datetime import datetime, timedelta
from fastapi import Depends
from typing import Optional
from jose import jwt, JWTError

SECRET_KEY = "1d93b4d3b57a045d760038ac65bc196b8bca73dc7bf9fa5650d812c40cfc9942"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_token(subject: str, expires_delta : Optional[timedelta] = None):
    to_encode = {"sub": str(subject)}
    expires = datetime.utcnow() + expires_delta if expires_delta else datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expires})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_token(token : str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    sub = payload.get("sub")
    if sub is None:
        raise JWTError("Missing sub claim")
    return schemas.TokenData(sub=sub)