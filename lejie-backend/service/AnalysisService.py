from fastapi import Depends
from service.Base import baseService
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from database.Base import GetDb
from database.UserInterfaceInfo import UserInterfaceInfoORM
from database.InterfaceInfo import InterfaceInfoORM
from schema.AnalysisSchema import InterfaceInfoBase


class analysisService(baseService):
    def __init__(self):
        pass

    def interfaceInvokeTotalNum(self, top: int = 3, db: Session = Depends(GetDb)):
        result = {'msg': 'success', 'ret': 0, 'data': []}
        try:
            query = db.query(
                UserInterfaceInfoORM.interfaceInfoId,
                func.sum(UserInterfaceInfoORM.totalNumber).label('totalNum')).group_by(
                    UserInterfaceInfoORM.interfaceInfoId
                ).order_by(desc('totalNum')).limit(top).all()

            interfaceInfoIdObjMap = {}
            for item in query:
                interfaceInfoIdObjMap[item.interfaceInfoId] = int(item.totalNum) # item.totalNum 被 func.sum 转换成 Decimal 类，用于表示固定精度的十进制数字

            interfaceInfoListQuery = db.query(InterfaceInfoORM).filter(
                InterfaceInfoORM.id.in_(interfaceInfoIdObjMap.keys())
            ).all()

            if not interfaceInfoListQuery:
                result['msg'], result['ret'] = '接口信息表查询错误，请检查其和关系表的数据一致性', 1
                return result
            for item in interfaceInfoListQuery:
                alalysisInterfaceInfoVO = InterfaceInfoBase(**item.__dict__)
                alalysisInterfaceInfoVO.totalNum = interfaceInfoIdObjMap[item.id]
                result['data'].append(alalysisInterfaceInfoVO)
        except Exception as e:
            print(f'error happen: {e}', flush=True)
            result['msg'], result['ret'] = f'操作失败：{e}', 1
        finally:
            return result
