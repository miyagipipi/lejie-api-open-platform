from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.Base import GetDb
from database.User import User
from schema import UserSchema
from typing import Annotated
from service import UserService


api = APIRouter(prefix='/user')
user_service = UserService.userService()


@api.post("/create/", response_model=UserSchema.User)
def userCreate(user: UserSchema.UserCreate, db: Session = Depends(GetDb)):
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@api.get("/getUserById/{user_id}", response_model=UserSchema.User)
def userGetUserById(user_id: int, db: Session = Depends(GetDb)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@api.post('/token')
async def loginForAccessToken(request: UserSchema.TokenRequest, db: Session = Depends(GetDb)) -> UserSchema.Token:
    return user_service.genToken(request, db)


@api.get('/current', response_model=UserSchema.UserResponse)
async def userCurrent(current_user: Annotated[UserSchema.UserInDBResponse, Depends(user_service.getCurrentUser)]):
    return current_user


@api.post('/register')
async def userRegister(result: Annotated[UserSchema.UserResponse, Depends(user_service.register)]):
    return result

@api.post('/email/register')
async def userRegister(result: Annotated[UserSchema.UserResponse, Depends(user_service.emailRegister)]):
    return result


@api.get('/getCaptcha')
async def userRegister(result: Annotated[UserSchema.NormalResponse, Depends(user_service.getCaptcha)]):
    return result


@api.post('/email/login')
def userEmaliLogin(result: Annotated[UserSchema.TokenResponse, Depends(user_service.emailLogin)]):
    return result