from sqlalchemy import Column, Integer, DateTime
from database.Base import Base, SessionLocal
from datetime import datetime


class UserInterfaceInfoORM(Base):
    __tablename__ = "user_interface_info"

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer)
    interfaceInfoId = Column(Integer)
    totalNumber = Column(Integer, default=0)
    leftNumber = Column(Integer, default=0)
    status = Column(Integer, default=0)
    createTime = Column(DateTime, default=datetime.now())
    updateTime = Column(DateTime, default=datetime.now())
    isDelete = Column(Integer, default=0)


def UserInterfaceInfoDbQuery():
    db = SessionLocal()
    try:
        yield db.query(UserInterfaceInfoORM).filter_by(isDelete=0)
    finally:
        db.close()
