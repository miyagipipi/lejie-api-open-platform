from datetime import datetime, timedelta, timezone
from typing import Annotated, Union

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel

from database.Base import GetDb
from sqlalchemy.orm import Session
from database.User import User as UserORM


api = APIRouter()

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = '3e6d15c08277329d5f30ce830b57b1a150a9da1619058067e14b16ef8ce20374'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str | None = None
    userAccount: str | None
    avatarUrl: str | None
    gender: int = 0
    phone: str | None
    email: str | None
    tags: str | None = "[]"
    profile: str | None
    createTime: datetime | None = None
    isDelete: int

class UserInDB(User):
    userPassword: str
    
    class Config:
        from_attributes = True


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/test/token')

### 密码哈希
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def verifyPassword(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def getPasswordHash(password):
    return pwd_context.hash(password)

def getUser(db: Session, userAccount: str):
    user_query = db.query(UserORM).filter_by(userAccount=userAccount).first()
    if user_query:
        # user_dict = user_query
        return UserInDB.model_validate(user_query)

def authenticateUser(db: Session, userAccount: str, password: str):
    user = getUser(db, userAccount)
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

async def getCurrentUser(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(GetDb)
):
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
        user = getUser(db, userAccount=username)
        if not user:
            raise credentials_exception
        return user
    except InvalidTokenError:
        raise credentials_exception

async def getCurrentActiveUser(current_user: Annotated[User, Depends(getCurrentUser)]):
    if current_user.isDelete:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@api.post('/token')
async def loginForAccessToken(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(GetDb)
) -> Token:
    user = authenticateUser(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = creatAccessToken(
        data={'sub': user.userAccount},
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
