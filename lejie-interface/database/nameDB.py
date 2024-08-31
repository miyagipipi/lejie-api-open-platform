from sqlalchemy import Column, Integer, String, Text, DateTime
from database.Base import Base, SessionLocal
from datetime import datetime


class InterfaceInfoORM(Base):
    __tablename__ = "interface_info"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    description = Column(String(255))
    userId = Column(Integer)
    url = Column(String(512))
    method = Column(String(255))
    requestHeader = Column(Text)
    responseHeader = Column(Text)
    status = Column(Integer, default=0)
    createTime = Column(DateTime, default=datetime.now())
    updateTime = Column(DateTime, default=datetime.now())
    isDelete = Column(Integer, default=0)


def Query():
    db = SessionLocal()
    try:
        yield db.query(InterfaceInfoORM).filter_by(isDelete=0)
    finally:
        db.close()
