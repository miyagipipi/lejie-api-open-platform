from fastapi import APIRouter, Depends
from schema.AnalysisSchema import InterfaceInfoListResponse
from typing import Annotated
from service.AnalysisService import analysisService


api = APIRouter(prefix='/analysis')
analysis_service = analysisService()


@api.get('/interface/top/invoke', response_model=InterfaceInfoListResponse)
def interfaceTopInvoke(result: Annotated[InterfaceInfoListResponse, Depends(analysis_service.interfaceInvokeTotalNum)]):
    return result

