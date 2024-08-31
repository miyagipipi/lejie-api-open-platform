from fastapi import Depends
from service.Base import baseService
from schema import nameSchema
from sqlalchemy.orm import Session
from database.nameDB import InterfaceInfoORM, Query
from database.Base import GetDb
from sqlalchemy.orm import Query as QueryType


class interfaceInfoService(baseService):
    """docstring for interfaceInfoService"""
    def __init__(self):
        self.table = InterfaceInfoORM

    
