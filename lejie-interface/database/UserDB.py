from sqlalchemy import Column, Integer, String, DateTime
from database.Base import Base
from datetime import datetime


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255))
    userAccount = Column(String(255))
    avatarUrl = Column(String(1024))
    gender = Column(Integer, default=0)
    userPassword = Column(String(512))
    accessKey = Column(String(512))
    secretKey = Column(String(512))
    phone = Column(String(128))
    email = Column(String(512))
    userStatus = Column(Integer, default=0)
    tags = Column(String(1024), default="[]")
    userRole = Column(Integer, default=0)
    profile = Column(String(512), default='')
    createTime = Column(DateTime, default=datetime.now())
    updateTime = Column(DateTime, default=datetime.now())
    isDelete = Column(Integer, default=0)
