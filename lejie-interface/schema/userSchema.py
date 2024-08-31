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

class UserInDBBase(UserBase):
    id: int

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserTest3(BaseModel):
    id: int
    username: Optional[str] = None
    userAccount: Optional[str]
    avatarUrl: Optional[str]
    gender: Optional[int] = 0
    phone: Optional[str]
    email: Optional[str]
    tags: Optional[str] = "[]"
    profile: Optional[str]
    userRole: int = 0
    
    class Config:
        from_attributes = True
