import rpyc
from rpyc.utils.server import ThreadedServer
from rpyc.core.protocol import DEFAULT_CONFIG
from config import BaseConfig
from service.Base import baseService
from database.Base import GetSession
from database.User import User as UserORM
from database.InterfaceInfo import InterfaceInfoORM
from database.UserInterfaceInfo import UserInterfaceInfoORM
import redis_lock
from redisClient import createRedisJobClient
from schema.UserSchema import UserInDB
from schema.InterfaceInfoSchema import Base as interfaceInfoBase


conn = createRedisJobClient()


def invokeCountLock(interfaceInfoId: int, userId: int) -> redis_lock.Lock:
    return redis_lock.Lock(
        conn,
        f'lejie:invokeCount:lock:{interfaceInfoId}-{userId}',
        expire=10,
        auto_renewal=True)


base_service = baseService()

protocol_config = DEFAULT_CONFIG.copy()
protocol_config["allow_public_attrs"] = True

class MyService(rpyc.Service):
    ALIASES = ["lejie-common"]
    
    def on_connect(self, conn):
        # code that runs when a connection is created
        # (to init the service, if needed)
        pass

    def on_disconnect(self, conn):
        # code that runs after the connection has already closed
        # (to finalize the service, if needed)
        pass

    @rpyc.exposed
    def getInvokeUser(self, accessKey: str):
        with GetSession() as db:
            data = db.query(UserORM).filter_by(accessKey=accessKey).first()
            return UserInDB(**data.__dict__).model_dump() if data else None

    @rpyc.exposed
    def getInterfaceInfo(self, url: str, method: str):
        with GetSession() as db:
            data = db.query(InterfaceInfoORM).filter_by(url=url, method=method).first()
            return interfaceInfoBase(**data.__dict__).model_dump() if data else None

    @rpyc.exposed
    def invokeCount(self, interfaceInfoId: int, userId: int):
        if interfaceInfoId <= 0 or userId <= 0:
            return False
        result = False
        try:
            with GetSession() as db:
                LOCK = invokeCountLock(interfaceInfoId, userId)
                if LOCK.acquire(blocking=False):
                    db.query(UserInterfaceInfoORM).filter_by(interfaceInfoId=interfaceInfoId, userId=userId).update({
                        "leftNumber": UserInterfaceInfoORM.leftNumber-1,
                        "totalNumber": UserInterfaceInfoORM.totalNumber+1,
                    })
                    db.commit()
                    result = True
                else:
                    result = False
        finally:
            if LOCK.locked():
                LOCK.release()
            return result

if __name__ == "__main__":
    server = ThreadedServer(
        MyService(),
        port=BaseConfig.RPyCPort,
        auto_register=True,
        protocol_config=protocol_config)

    server.start()