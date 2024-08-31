from pydantic import BaseModel
from schema.InterfaceInfoSchema import Base
from typing import List


class InterfaceInfoBase(Base):
    totalNum: int = 0
    
    class Config:
        from_attributes = True

class InterfaceInfoListResponse(BaseModel):
    msg: str
    ret: int
    data: List[InterfaceInfoBase]
