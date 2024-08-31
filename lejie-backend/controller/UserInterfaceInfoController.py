from fastapi import APIRouter, Depends
from schema import UserInterfaceInfoSchema
from typing import Annotated
from service.UserInterfaceInfoService import userInterfaceInfoService


api = APIRouter(prefix='/userInterfaceInfo')
user_interfaceInfo_service = userInterfaceInfoService()


@api.post('/add', response_model=UserInterfaceInfoSchema.NormalResponse)
def userInterfaceInfoAdd(result: Annotated[UserInterfaceInfoSchema.NormalResponse, Depends(user_interfaceInfo_service.add)]):
    return result


@api.post('/delete', response_model=UserInterfaceInfoSchema.NormalResponse)
def userInterfaceInfoDelete(result: Annotated[UserInterfaceInfoSchema.NormalResponse, Depends(user_interfaceInfo_service.deleteByID)]):
    return result


@api.post('/update', response_model=UserInterfaceInfoSchema.NormalResponse)
async def userInterfaceInfoUpdate(result: Annotated[UserInterfaceInfoSchema.NormalResponse, Depends(user_interfaceInfo_service.update)]):
    return result


@api.get('/getById/{_id}', response_model=UserInterfaceInfoSchema.NormalResponse)
async def userInterfaceInfoGetById(result: Annotated[UserInterfaceInfoSchema.NormalResponse, Depends(user_interfaceInfo_service.getById)]):
    return result


"""
校验
    接口和用户存在
    剩余调用次数不能小于 0
"""