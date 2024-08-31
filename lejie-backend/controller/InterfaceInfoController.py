from fastapi import APIRouter, Depends, Header
from schema import InterfaceInfoSchema
from typing import Annotated
from service.InterfaceInfoService import interfaceInfoService
from util import TokenUtil
from sqlalchemy.orm import Session
from database.Base import GetDb, GetAsyncDB


api = APIRouter(prefix='/interfaceInfo')
interfaceInfo_service = interfaceInfoService()


@api.post('/page')
def interfaceInfoPage(result: Annotated[InterfaceInfoSchema.PageRequest, Depends(interfaceInfo_service.getPage)]):
    return result


@api.post('/add', response_model=InterfaceInfoSchema.NormalResponse)
def interfaceInfoAdd(result: Annotated[InterfaceInfoSchema.AddReuqest, Depends(interfaceInfo_service.add)]):
    return result


@api.post('/delete', response_model=InterfaceInfoSchema.NormalResponse)
def interfaceInfoDelete(result: Annotated[InterfaceInfoSchema.IdModel, Depends(interfaceInfo_service.deleteByID)]):
    return result


@api.post('/update', response_model=InterfaceInfoSchema.NormalResponse)
async def interfaceInfoUpdate(result: Annotated[InterfaceInfoSchema.NormalResponse, Depends(interfaceInfo_service.update)]):
    return result


@api.get('/getById/{_id}')
async def interfaceInfoGetById(result: Annotated[InterfaceInfoSchema.NormalResponse, Depends(interfaceInfo_service.getById)]):
    return result


@api.post('/online')
async def interfaceInfoOnline(
    request: InterfaceInfoSchema.IdModel,
    authorization: Annotated[str | None, Header()] = '',
    db: Session = Depends(GetDb)
):
    userAccount = TokenUtil.getUsernameByToken(authorization.split(' ')[-1])
    loginUser = interfaceInfo_service.getUser(db, userAccount)
    return await interfaceInfo_service.setApiOnline(request, loginUser, db)


@api.post('/offline', response_model=InterfaceInfoSchema.NormalResponse)
async def interfaceInfoOffline(
    request: InterfaceInfoSchema.IdModel,
    authorization: Annotated[str | None, Header()] = '',
    db: Session = Depends(GetDb)
):
    userAccount = TokenUtil.getUsernameByToken(authorization.split(' ')[-1])
    loginUser = interfaceInfo_service.getUser(db, userAccount)
    return await interfaceInfo_service.setApiOffline(request, loginUser, db)

@api.post('/invoke', response_model=InterfaceInfoSchema.NormalResponse)
async def interfaceInfoInvoke(
    request: InterfaceInfoSchema.InvokeRequest,
    authorization: Annotated[str | None, Header()] = '',
    db: Session = Depends(GetDb)):
    loginUser = interfaceInfo_service.getUser(db, TokenUtil.getUsernameByToken(authorization.split(' ')[-1]))
    return await interfaceInfo_service.invoke(request, loginUser, db)
