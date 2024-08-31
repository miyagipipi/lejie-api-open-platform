from fastapi import Depends
from service.Base import baseService
from schema import InterfaceInfoSchema, UserSchema
from sqlalchemy.orm import Session
from database.InterfaceInfo import InterfaceInfoORM, Query
from database.Base import GetDb
from sqlalchemy.orm import Query as QueryType
from lejie_client import LejieApiClient



class interfaceInfoService(baseService):
    """docstring for interfaceInfoService"""
    def __init__(self):
        self.table = InterfaceInfoORM
        self.schema = InterfaceInfoSchema.InterfaceInfoDB
    
    def getById(self, _id: int, db: Session = Depends(GetDb)):
        return super().getById(_id, db)

    def getPage(self, request: InterfaceInfoSchema.PageRequest, db: QueryType = Depends(Query)):
        # 判断是否登录的逻辑
        # todo
        result = {'msg': 'success', 'ret': 0, 'data': []}
        pagesize = request.pageSize
        current = request.current
        offset = (current - 1) * pagesize
        total = db.count()
        result['total'] = total
        query = db.limit(pagesize).offset(offset).all()
        for item in query:
            result['data'].append(item)
        return result

    def add(self, request: InterfaceInfoSchema.AddReuqest, db: Session = Depends(GetDb)):
        result = {'msg': 'success', 'ret': 0, 'data': {}}
        try:
            new_item = InterfaceInfoORM(**request.model_dump())
            db.add(new_item)
            db.commit()
            _id = new_item.id
            if _id:
                result['data']['id'] = _id
            else:
                result['msg'], result['ret'] = '创建失败', 1
        except Exception as e:
            print(f'error happen: {e}', flush=True)
            result['msg'], result['ret'] = f'操作失败：{e}', 1
        finally:
            return result
    
    def update(self, request: InterfaceInfoSchema.updateRequest, db: Session = Depends(GetDb)):
        result = {'msg': 'success', 'ret': 0, 'data': {}}
        try:
            _id = request.id
            query = db.query(self.table).filter_by(id=_id, isDelete=0).first()
            if not query:
                result['msg'], result['ret'] = '操作失败，未在数据库中查询到', 1
                return result
            for key, value in request.model_dump().items():
                if key != 'id' and getattr(query, key) != value:
                    setattr(query, key, value)
            db.commit()
        except Exception as e:
            print(f'error happen: {e}', flush=True)
            result['msg'], result['ret'] = f'操作失败：{e}', 1
            db.rollback()
        finally:
            return result
    
    def deleteByID(self, request: InterfaceInfoSchema.IdModel, db: Session = Depends(GetDb)):
        result = {'msg': 'success', 'ret': 0}
        try:
            _id = request.id
            data = db.query(InterfaceInfoORM).get(_id)
            if data:
                data.isDelete = 1
                db.commit()
            else:
                result['msg'], result['ret'] = '删除失败', 1
        except Exception as e:
            print(f'error happen: {e}', flush=True)
            result['msg'], result['ret'] = f'操作失败：{e}', 1
        finally:
            return result
    
    async def setApiOnline(
        self,
        request: InterfaceInfoSchema.IdModel,
        current_user: UserSchema.UserInDB,
        db: Session = Depends(GetDb)
    ):
        result = {'msg': 'success', 'ret': 0}
        try:
            if not request or request.id <= 0:
                result['msg'], result['ret'] = '请求参数错误', 1
                return result
            _id = request.id
            InterfaceInfoData = db.query(InterfaceInfoORM).filter_by(id=_id, isDelete=0).first()
            if not InterfaceInfoData:
                result['msg'], result['ret'] = '接口不存在', 1
                return result
            lejieApiClient = LejieApiClient('lejie', 'tianxiao', 'localhost', 5177)
            # todo 修改接口验证逻辑 这里在加入网关和中间件后 会导致用户的调用次数无感知地 + 1
            # username = lejieApiClient.getUsernameByPost('tianxiao')
            # if not username:
            #     result['msg'], result['ret'] = '接口验证失败', 1
            #     return result
            if not current_user.id:
                result['msg'], result['ret'] = '用户信息获取错误', 1
                return result
            if current_user.id != InterfaceInfoData.userId and current_user.userRole != 1:
                result['msg'], result['ret'] = '无权操作此接口', 1
                return result
            InterfaceInfoData.status = 1
            db.commit()
        except Exception as e:
            print(f'error happen: {e}', flush=True)
            result['msg'], result['ret'] = f'操作失败：{e}', 1
            db.rollback()
        finally:
            return result

    async def setApiOffline(
        self,
        request: InterfaceInfoSchema.IdModel,
        current_user: UserSchema.UserInDB,
        db: Session = Depends(GetDb)
    ):
        result = {'msg': 'success', 'ret': 0}
        try:
            if not request or request.id <= 0:
                result['msg'], result['ret'] = '请求参数错误', 1
                return result
            _id = request.id
            InterfaceInfoData = db.query(InterfaceInfoORM).filter_by(id=_id, isDelete=0).first()
            if not InterfaceInfoData:
                result['msg'], result['ret'] = '接口不存在', 1
                return result
            if not current_user.id:
                result['msg'], result['ret'] = '用户信息获取错误', 1
                return result
            if current_user.id != InterfaceInfoData.userId and current_user.userRole != 1:
                result['msg'], result['ret'] = '无权操作此接口', 1
                return result
            InterfaceInfoData.status = 0
            db.commit()
        except Exception as e:
            print(f'error happen: {e}', flush=True)
            result['msg'], result['ret'] = f'操作失败：{e}', 1
            db.rollback()
        finally:
            return result
    
    async def invoke(
        self,
        request: InterfaceInfoSchema.InvokeRequest,
        loginUser: UserSchema.UserInDB | None,
        db: Session = Depends(GetDb)):
        result = {'msg': 'success', 'ret': 0, 'data': {}}
        try:
            requestParams = request.requestParams
            _id = request.id
            if not loginUser:
                result['msg'], result['ret'] = f'用户未登录', 1
                return result
            oldInterfaceInfo = db.query(InterfaceInfoORM).filter_by(id=_id).first()
            if not oldInterfaceInfo or oldInterfaceInfo.status == 0:
                result['msg'], result['ret'] = f'接口不存在或已关闭', 1
                return result
            accessKey, secretKey = loginUser.accessKey, loginUser.secretKey
            lejieApiClient = LejieApiClient(accessKey, secretKey)
            client_res = lejieApiClient.getUsernameByPost(requestParams)
            result['msg'] = client_res.text
            if not client_res.ok:
                result['ret'] = 1
        except Exception as e:
            print(f'error happen: {e}', flush=True)
            result['msg'], result['ret'] = f'操作失败：{e}', 1
            db.rollback()
        finally:
            return result
