from datetime import datetime, timedelta

import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

# Конфигурация для Auth
SECRET_KEY = "KVAZISTAM"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



# OAuth2 token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt