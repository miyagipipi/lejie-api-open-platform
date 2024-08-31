from fastapi import Depends
from service.Base import baseService
from schema import UserInterfaceInfoSchema
from sqlalchemy.orm import Session
from database.UserInterfaceInfo import UserInterfaceInfoORM
from database.Base import GetDb


class userInterfaceInfoService(baseService):
    def __init__(self):
        self.table = UserInterfaceInfoORM
        self.schema = UserInterfaceInfoSchema.DbModel
    
    async def getById(self, _id: int, db: Session = Depends(GetDb)):
        return super().getById(_id, db)

    async def add(self, request: UserInterfaceInfoSchema.Add, db: Session = Depends(GetDb)):
        result = {'msg': 'success', 'ret': 0, 'data': {}}
        try:
            new_item = UserInterfaceInfoORM(**request.model_dump())
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
    
    """
    deleteByID -> BaseService.py
    def baseDeleteById(self, request: normalIdModel, db = ...):
        ...
        UserInterfaceInfoORM -> self.table
    """
    async def deleteByID(self, request: UserInterfaceInfoSchema.IdModel, db: Session = Depends(GetDb)):
        result = {'msg': 'success', 'ret': 0}
        try:
            _id = request.id
            data = db.query(UserInterfaceInfoORM).filter_by(id=_id, isDelete=0).first()
            if data:
                data.isDelete = 1
                db.commit()
            else:
                result['msg'], result['ret'] = '删除失败，数据已删除或不存在', 1
        except Exception as e:
            print(f'error happen: {e}', flush=True)
            result['msg'], result['ret'] = f'操作失败：{e}', 1
        finally:
            return result
    
    async def update(self, request: UserInterfaceInfoSchema.UpdateRequest, db: Session = Depends(GetDb)):
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

