from fastapi import FastAPI, Request, HTTPException, Response, status
import uvicorn
from controller import nameController
from config import CorsConfig, BaseConfig
from database.Base import GetSession
from sqlalchemy.orm import Session
from util import SignUtil
import time
import rpyc


app = FastAPI()
CorsConfig.init(app)


app.include_router(nameController.api, tags=['name'])



def beforeCheck(request: Request, rc):
    result = {'msg': '', 'ret': True}
    
    # todo 随机数校验（缓存）
    accessKey = request.headers.get('accessKey')
    nonce = request.headers.get('nonce')
    timestamp = int(request.headers.get('timestamp'))
    sign = request.headers.get('sign')
    body = request.headers.get('body') # userAccount

    
    # path 的获取应该由 HOST 常量 + 请求的 path 组成
    path = request.url
    # print(request.base_url)
    # print(request.path_params)
    """
    INTERFACE_HOST = "hppt://localhost:port"
    path = INTERFACE_HOST + request.headers.get('path)
    """
    
    method = request.method
    
    # 时间戳过期校验
    currentTime = int(time.time())
    if currentTime - timestamp > 60 * 5:
        result['msg'], result['ret'] = '请求的时间戳已过期', False
        return result
    
    invokeUser = rc.root.getInvokeUser(accessKey)
    if not invokeUser:
        result['msg'], result['ret'] = '用户无权限', False
        return result
    
    secretKeyInDb = invokeUser['secretKey']
    serverSign = SignUtil.genSign(body, secretKeyInDb)
    if serverSign != sign:
        result['msg'], result['ret'] = '密钥错误，无权限调用', False
        return result
    
    # 请求的模拟接口是否存在
    interfaceInfo = rc.root.getInterfaceInfo(str(path), method)
    if not interfaceInfo:
        result['msg'], result['ret'] = '接口不存在', False
        return result
    
    # todo 是否还有可调用次数的校验

    # 补充给 afterCheck 使用
    result['userId'], result['interfaceInfoId'] = invokeUser['id'], interfaceInfo['id']

    return result


def invokeCheck(rc, beforeCheckResult) -> bool:
    return rc.root.invokeCount(beforeCheckResult['userId'], beforeCheckResult['interfaceInfoId'])


def afterCheck(request: Request, response: Response, rc, beforeCheckResult):
    result = {'msg': '', 'ret': True}
    try:
        invokeCheckResult = invokeCheck(rc, beforeCheckResult)
        if not invokeCheckResult:
            result['msg'], result['ret'] = 'invoke 统计失败', False
            return result
    finally:
        return result


@app.middleware("http")
async def globalCheck(request: Request, call_next):
    if not rpyc.discover(BaseConfig.rpyc_serve):
        print(f'common server [{BaseConfig.rpyc_serve}] not be discovered')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='common rpc server not be discovered')
    try:
        rc = rpyc.connect_by_service(BaseConfig.rpyc_serve)
        beforeCheckResult = beforeCheck(request, rc)
        if not beforeCheckResult['ret']:
            raise HTTPException(status_code=401, detail=beforeCheckResult['msg'])
        
        response = await call_next(request)

        # todo 调用成功后，次数 + 1
        afterCheckResult = afterCheck(request, response, rc, beforeCheckResult)
        if not afterCheckResult['ret']:
            raise HTTPException(status_code=401, detail=afterCheckResult['msg'])
        return response
    finally:
        if not rc.closed:
            rc.close()


if __name__ == '__main__':
    uvicorn.run(
        app='app:app',
        host=BaseConfig.host,
        port=BaseConfig.port,
        reload=BaseConfig.reload
    )
