from fastapi import Depends
from sqlalchemy.orm import Session
from database.User import User as UserORM
from database.Base import GetDb
from schema import UserSchema
from typing import Annotated
from config.JwtConfig import OAUTH2_SCHEME
from util import TokenUtil
from pydantic import BaseModel



class baseService(object):
    def __init__(self) -> None:
        self.table = None
        self.schema = None
    
    def setTabele(self, table):
        self.table = table
    
    def setSchema(self, schema: BaseModel):
        self.schema = schema
    
    def getById(self, _id: int, db: Session = Depends(GetDb)) -> dict:
        result = {'msg': 'success', 'ret': 0, 'data': {}}
        try:
            if not self.table:
                result['msg'], result['ret'] = '操作失败，tableORM 未设置', 1
                return result
            if not self.schema:
                result['msg'], result['ret'] = '操作失败，pydantic-scheme 未设置', 1
                return result
            query = db.query(self.table).get(_id)
            if not query:
                result['msg'], result['ret'] = '操作失败，对应的数据不存在', 1
                return result
            model = self.schema(**query.__dict__)
            result['data'] = model.model_dump()
        except Exception as e:
            print(f'error happen: {e}', flush=True)
            result['msg'], result['ret'] = f'操作失败：{e}', 1
        finally:
            return result
    
    def getUser(self, db: Session, userAccount: str) -> UserSchema.UserInDB | None:
        user_query = db.query(UserORM).filter_by(userAccount=userAccount).first()
        return UserSchema.UserInDB.model_validate(user_query) if user_query else None

    def getCurrentUser(
        self,
        token: Annotated[str, Depends(OAUTH2_SCHEME)],
        db: Session = Depends(GetDb)
    ):
        result = {'msg': '成功', 'ret': 0}
        try:
            username: str = TokenUtil.getUsernameByToken(token)
            if not username:
                result['msg'], result['ret'] = 'token验证未通过', 1
                return result
            user = self.getUser(db, username)
            if not user:
                result['msg'], result['ret'] = '用户不存在，请重新登录', 1
                return result
            result['data'] = user
        except Exception as e:
            print(f'error happen: {e}', flush=True)
            result['msg'], result['ret'] = f'操作失败：{e}', 1
        finally:
            return result
    