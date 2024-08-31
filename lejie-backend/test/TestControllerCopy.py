from datetime import datetime, timedelta, timezone
from typing import Annotated, Union

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel


api = APIRouter()

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = '3e6d15c08277329d5f30ce830b57b1a150a9da1619058067e14b16ef8ce20374'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/test/token')

### 密码哈希
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def verifyPassword(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def getPasswordHash(password):
    return pwd_context.hash(password)

def getUser(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticateUser(fake_db, username: str, password: str):
    user = getUser(fake_db, username)
    if not user:
        return False
    if not verifyPassword(password, user.hashed_password):
        return False
    return user

def creatAccessToken(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
###

async def getCurrentUser(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if not username:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = getUser(fake_users_db, username=username)
    if not user:
        raise credentials_exception
    return user

async def getCurrentActiveUser(current_user: Annotated[User, Depends(getCurrentUser)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@api.post('/token')
async def loginForAccessToken(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = authenticateUser(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = creatAccessToken(
        data={'sub': user.username},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type='bearer')
    
@api.get('/me/', response_model=User)
async def userMe(current_user: User = Depends(getCurrentActiveUser)):
    return current_user

@api.get("/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(getCurrentActiveUser)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]
