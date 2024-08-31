from fastapi import APIRouter
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    
class UserAccount(BaseModel):
    userAccount: str


api = APIRouter(prefix='/api/name')



@api.get('/')
async def nameGet(name: str):
    return f'GET 你的名字是 {name}'


@api.post('/')
async def namePost(item: Item):
    name = item.name
    return f"POST 你的名字是 {name}"


@api.post('/userAccount')
async def nameUser(data: UserAccount):
    result = f"POST 你的名字是 {data.userAccount}"
    return result
