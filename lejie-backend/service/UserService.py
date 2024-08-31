from fastapi import Depends, HTTPException, status
from service.Base import baseService
from schema import UserSchema
from sqlalchemy.orm import Session
from datetime import timedelta
from config.JwtConfig import ACCESS_TOKEN_EXPIRE_MINUTES
from util import TokenUtil, CheckUtil
from database.User import User as UserORM
from database.Base import GetDb
from typing import Annotated
import hashlib, random


SALT = "zest"

class userService(baseService):
    """docstring for userService"""
    def __init__(self):
        self.schema = UserSchema.UserBase
        self.inDB = UserSchema.UserInDB
    
    def genToken(self, form_data: UserSchema.TokenRequest, db: Session) -> UserSchema.Token:
        user = self.authenticateUser(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = TokenUtil.creatAccessToken(
            data={'sub': user.userAccount},
            expires_delta=access_token_expires
        )
        return UserSchema.Token(access_token=access_token, token_type='bearer', ret=0)

    def authenticateUser(self, db: Session, userAccount: str, password: str):
        user = self.getUser(db, userAccount)
        if not user:
            return False
        if not TokenUtil.verifyPassword(password, user.userPassword):
            return False
        return user
    
    async def register(self, request: UserSchema.UserRegistr, db: Session = Depends(GetDb)):
        result = {'msg': 'success', 'ret': 0, 'data': {}}
        try:
            userAccount, userPassword, checkPassword = request.userAccount, request.userPassword, request.checkPassword
            check_result = CheckUtil.checkUserRegister(userAccount, userPassword, checkPassword)
            if check_result['ret'] == 1:
                result = check_result
                return result
            count = db.query(UserORM).filter_by(userAccount=userAccount).count()
            if count > 0:
               result['msg'], result['ret'] = f'用户已存在', 1
               return result
            hashed_password = TokenUtil.getPasswordHash(userPassword)
            accessKey = hashlib.sha256(f"{SALT}.{userAccount}.{random.randint(0, 10000)}".encode()).hexdigest()
            secretKey = hashlib.sha256(f"{SALT}.{userAccount}.{random.randint(10001, 10000000)}".encode()).hexdigest()
            user = UserORM(
                userAccount=userAccount,
                userPassword=hashed_password,
                accessKey=accessKey,
                secretKey=secretKey
            )
            db.add(user)
            db.commit()
            db.refresh
            result['data']['id'] = user.id
        except Exception as e:
            print(f'error happen: {e}', flush=True)
            result['msg'], result['ret'] = f'操作失败：{e}', 1
        finally:
            return result
    """
    @PostMapping('/register')
public BaseRseponse<Long> userRegister(@RequestBody UserRegisterResques userRegisterResques) {
    if (userRegisterResques == null) {
        throw new PARAMS_ERROR
    }
    String userAccount = userRegisterResques.getUserAccount()
    String userPassword = userRegisterResques.getUserPassword()
    String checkPassword = userRegisterResques.getCheckPassword()
    if (StringUtils.isAnyBlank(userAccount, userPassword, checkPassword)) {
        return null
    }
    long result = userService.userRegister(userAccount, userPassword, checkPassword)
    return ResultUtils.success(result)
}

    SALT = "yupi"
    """

    """
public long userRegister(String userAccount, String userPassword, String checkPassword) {
    // 校验
    if (StringUtils.isAnyBlank(userAccount, userPassword, checkPassword)) {
        return null
    }
    if (userAccount.length() < 4) {
        throw new "用户账号过短"
    }
    if (userPassword.length() < 8 || checkPassword.length() < 8) {
        throw new "用户密码过短"
    }
    if (!userPassword.equals(checkPassword)) {
        throw new "两次输入的密码不一致"
    }
    synchronized (userAccount.intern()) {
        // 账号不能重复
        QueryWrapper<User> queryWrapper = new QueryWrapper<>()
        queryWrapper.eq("userAccount", userAccount)
        long count = uuserMapper.selectCount(QueryWrapper)
        if (count > 0) {
            throw new "账号已存在"
        }
        // 加密
        String encryptPassword = DigestUtils.md5DigestAsHex((SALT + userPassword).getBytes())
        //分配 ak, sk 加密算法生成
        String accessKey = DigestUtils.md5(SALT + userAccount + RandomUtil.randomNumber(length = 5))
        String secretKey = DigestUtils.md5(SALT + userAccount + RandomUtil.randomNumber(length = 8))
        // 加入数据
        User user = new User()
        user.setUserAccount(userAccount)
        // set password, accessKey, secretKey
        boolean saveResult = this.save(user)
        if (!saveResult) {
            throw new "注册失败，数据库错误"
        }
        return user.getId()
    }
}

    """
