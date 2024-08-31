from fastapi import FastAPI
import uvicorn
from controller import (
    UserController, InterfaceInfoController, UserInterfaceInfoController,
    AnalysisController)
from config import CorsConfig, BaseConfig


app = FastAPI()
CorsConfig.init(app)

app.include_router(UserController.api, tags=['User'])
app.include_router(InterfaceInfoController.api, tags=['Interface_Info'])
app.include_router(UserInterfaceInfoController.api, tags=['User_Interface_Info'])
app.include_router(AnalysisController.api, tags=['Analysis'])


if __name__ == '__main__':
    uvicorn.run(
        app='app:app',
        host=BaseConfig.host,
        port=BaseConfig.port,
        reload=BaseConfig.reload
    )
