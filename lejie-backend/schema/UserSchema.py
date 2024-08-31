from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    id: int
    username: Optional[str] = None
    userAccount: Optional[str]
    avatarUrl: Optional[str]
    gender: Optional[int] = 0
    phone: Optional[str]
    email: Optional[str]
    tags: Optional[str] = "[]"
    profile: Optional[str]
    createTime: Optional[datetime] = None
    userRole: int = 0

class UserCreate(BaseModel):
    username: str
    userAccount: str
    userPassword: str
    gender: int
    phone: str
    email: str

class UserLogin(BaseModel):
    userAccount: str
    userPassword: str

class UserInDBBase(UserBase):
    id: int

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserResponse(BaseModel):
    msg: str = 'success'
    ret: int = 0
    data: UserBase = {}

class UserInDB(UserBase):
    id: int
    userPassword: str
    accessKey: str
    secretKey: str
    class Config:
        from_attributes = True

class UserInDBResponse(BaseModel):
    msg: str = 'success'
    ret: int = 0
    data: UserInDB = {}
    
class Token(BaseModel):
    access_token: str
    token_type: str
    ret: int = 0

class TokenResponse(BaseModel):
    msg: str = 'success'
    ret: int = 0
    data: Token = {}

class TokenRequest(BaseModel):
    username: str
    password: str

class UserRegistr(UserLogin):
    checkPassword: str
