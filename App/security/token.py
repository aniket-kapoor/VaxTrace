import jwt
from jose import JWTError, jwt

from datetime import datetime, timedelta, timezone
from ..schemas import user 

#This code is generating a signed token which later will be used for authorization
from ..core.config import settings

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def verify_token(tok:str , credentials_exception):
        try:
            payload = jwt.decode(tok, settings.secret_key, algorithms=[settings.algorithm])
            email = payload.get("sub")
            if email is None:
                raise credentials_exception
           
            return user.TokenData(email=email) #correction
        except JWTError:
            raise credentials_exception

