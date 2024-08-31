from pydantic import BaseModel
from datetime import datetime


class Base(BaseModel):
    # id: int
    # userId: int
    # interfaceInfoId: int
    totalNumber: int
    leftNumber: int
    status: int = 0
    # createTime: datetime | None
    # updateTime: datetime | None
    # isDelete: int

class DbModel(Base):
    id: int
    userId: int
    interfaceInfoId: int
    createTime: datetime | None
    updateTime: datetime | None
    isDelete: int = 0

    class Config:
        from_attributes = True
        
class Add(Base):
    userId: int
    interfaceInfoId: int

    class Config:
        from_attributes = True

class NormalResponse(BaseModel):
    msg: str
    ret: int
    data: dict = {}
    
class UpdateRequest(Base):
    id: int

    class Config:
        from_attributes = True

class IdModel(BaseModel):
    id: int
