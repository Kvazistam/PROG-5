import asyncio
from datetime import timedelta
import jwt
from fastapi import Depends, HTTPException, status, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from Auth.Access_token import oauth2_scheme, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from Users.Models import User
from Users.users_db import get_user

app = FastAPI()


def authenticate_user(username: str, password: str, table="users"):
    """Проверяет правильность пароля, по идее можно кэшировать пароли, но в тз не требуется"""
    user = get_user(username, table=table)
    if  user and user.password == password:
        return user
    return False


async def get_current_user(token: str = Depends(oauth2_scheme), table="users",):
    """Получает пользователя из бд users по токену"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = get_user(username, table=table)
        if user is None:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise credentials_exception
    return user



@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), table="users"):
    user = authenticate_user(form_data.username, form_data.password, table=table)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}


@app.get("/spending")
async def read_salary(current_user: User = Depends(get_current_user)):
    return {"spending(RUB)": current_user.spending, "cashback(%)": current_user.cashback, "cashback level": current_user.cashback_level}
