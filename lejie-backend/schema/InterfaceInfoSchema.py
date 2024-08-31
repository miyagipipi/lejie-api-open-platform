from pydantic import BaseModel
from datetime import datetime
from typing import List


class Base(BaseModel):
    id: int
    name: str
    description: str
    userId: int
    url: str
    method: str
    requestParams: str
    requestHeader: str
    responseHeader: str
    status: int = 0
    createTime: datetime | None
    updateTime: datetime | None
    # isDelete: int

class InterfaceInfoDB(Base):
    id: int

    class Config:
        from_attributes = True

class PageRequest(BaseModel):
    pageSize: int = 10 # 每页显示的记录数
    current: int = 1 # 当前页码

class PageResponse(BaseModel):
    msg: str
    ret: int
    total: int
    data: List[Base]

class AddReuqest(BaseModel):
    name: str
    description: str
    userId: int
    url: str
    method: str
    requestParams: str
    requestHeader: str
    responseHeader: str
    status: int = 0

class NormalResponse(BaseModel):
    msg: str
    ret: int
    data: dict = {}

class IdModel(BaseModel):
    id: int

class updateRequest(BaseModel):
    id: int
    name: str
    description: str
    url: str
    method: str
    requestParams: str
    requestHeader: str
    responseHeader: str
    
class RequestParams(BaseModel):
    userAccount: str

class InvokeRequest(BaseModel):
    id: int
    requestParams: RequestParams
    
