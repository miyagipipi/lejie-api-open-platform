from fastapi import Depends, HTTPException, status, Query, Header
from service.Base import baseService
from schema import UserSchema
from sqlalchemy.orm import Session
from config.JwtConfig import ACCESS_TOKEN_EXPIRE_MINUTES
from config import EmailConfig
from util import TokenUtil, CheckUtil, CommonUtil
from database.User import User as UserORM
from database.Base import GetDb
from redisClient import createRedisCaptchaClient
from datetime import timedelta
import hashlib, random, ssl
import yagmail
from typing import Annotated


SALT = "zest"
redisCaptchaConn = createRedisCaptchaClient()


class userService(baseService):
    context = ssl.create_default_context()
    context.set_ciphers('DEFAULT')
            
    def __init__(self):
        self.schema = UserSchema.UserBase
        self.inDB = UserSchema.UserInDB
    
    def genToken(self, form_data: UserSchema.TokenRequest, db: Session) -> UserSchema.Token:
        user = self.authenticateUser(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="账号或密码不正确",
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
    
    # region 账号登录
    async def register(self, request: UserSchema.UserRegistr, db: Session = Depends(GetDb)):
        result = {'msg': 'success', 'ret': 0, 'data': {}}
        try:
            userAccount, username = request.userAccount, request.username
            userPassword =  request.userPassword
            check_result = CheckUtil.checkUserRegister(request)
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
                username=username,
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
            db.rollback()
            return result
    
    # region 邮箱注册
    async def emailRegister(self, request: UserSchema.UserEmailRegistr, db: Session = Depends(GetDb)):
        result = {'msg': 'success', 'ret': 0, 'data': {}}
        try:
            emailAccount, username = request.emailAccount, request.username
            captcha = request.captcha
            if not CheckUtil.checkEmailFormat(emailAccount):
                result['msg'], result['ret'] = '不合法的邮箱地址', 1
                return result
            
            cacheCaptcha = redisCaptchaConn.get(f'captcha:{emailAccount}').decode('utf-8')
            if not cacheCaptcha:
                result['msg'], result['ret'] = '验证码已过期，请重新获取', 1
                return result
            if captcha != cacheCaptcha:
                result['msg'], result['ret'] = '输入的验证码有误', 1
                return result
            
            count = db.query(UserORM).filter_by(email=emailAccount).count()
            if count > 0:
               result['msg'], result['ret'] = f'邮箱已被注册', 1
               return result

            # 需要生成随机账号和随机密码
            randomPassword = str(CommonUtil.randomNumbers(8))
            hashedPassword = TokenUtil.getPasswordHash(randomPassword)
            randomUserAccount = CommonUtil.genRandomUserAccount(12)
            accessKey = hashlib.sha256(f"{SALT}.{randomUserAccount}.{random.randint(0, 10000)}".encode()).hexdigest()
            secretKey = hashlib.sha256(f"{SALT}.{randomUserAccount}.{random.randint(10001, 10000000)}".encode()).hexdigest()
            user = UserORM(
                username=username,
                userAccount=randomUserAccount,
                userPassword=hashedPassword,
                accessKey=accessKey,
                secretKey=secretKey,
                email=emailAccount
            )
            db.add(user)
            db.commit()
            db.refresh
            redisCaptchaConn.delete(f'captcha:{emailAccount}')
            result['data']['id'] = user.id
            
        except Exception as e:
            print(f'error happen: {e}', flush=True)
            result['msg'], result['ret'] = f'操作失败：{e}', 1
        finally:
            db.rollback()
            return result

    # region 获取验证码
    async def getCaptcha(self, emailAccount: str = Query(regex=EmailConfig.EMAIL_REGEX)):
        result = {'msg': 'success', 'ret': 0, 'data': {}}
        try:
            captcha = CommonUtil.randomNumbers(6)

            yag=yagmail.SMTP(
                user=EmailConfig.FORM,
                password=EmailConfig.PASSWORD,
                host=EmailConfig.HOST,
                context=self.context)
            yag.send(to=emailAccount, subject=EmailConfig.SUBJECT, contents=f'您的验证码是\n {captcha}')
            redisCaptchaConn.set(f'captcha:{emailAccount}', captcha, ex=5*60)
        except Exception as e:
            print(f'error happen: {e}', flush=True)
            result['msg'], result['ret'] = f'操作失败：{e}', 1
        finally:
            if not yag.is_closed:
                yag.close()
            return result
    
    # region 邮箱登录
    async def emailLogin(self, request: UserSchema.EmailLoginRequest, db: Session = Depends(GetDb)):
        result = {'msg': 'success', 'ret': 0, 'data': {}}
        try:
            emailAccount, captcha = request.emailAccount, request.captcha
            if not CheckUtil.checkEmailFormat(emailAccount):
                result['msg'], result['ret'] = '不合法的邮箱地址', 1
                return result
            cacheCaptcha = redisCaptchaConn.get(f'captcha:{emailAccount}').decode('utf-8')
            if not cacheCaptcha:
                result['msg'], result['ret'] = '验证码已过期，请重新获取', 1
                return result
            if captcha != cacheCaptcha:
                result['msg'], result['ret'] = '输入的验证码有误', 1
                return result
            user = db.query(UserORM).filter_by(email=emailAccount).first()
            if not user:
                result['msg'], result['ret'] = '账号不存在或未绑定邮箱', 1
                return result
            # todo 0 改为 Emnu 类
            if user.userStatus != 0:
                result['msg'], result['ret'] = '账号非正常状态', 1
                return result
            # 和账号密保登模式一样生成一个 JWT
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = TokenUtil.creatAccessToken(
                data={'sub': user.userAccount},
                expires_delta=access_token_expires
            )
            result['data'] = UserSchema.Token(access_token=access_token, token_type='bearer', ret=0)
            redisCaptchaConn.delete(f'captcha:{emailAccount}')
        except Exception as e:
            print(f'error happen: {e}', flush=True)
            result['msg'], result['ret'] = f'操作失败：{e}', 1
        finally:
            return result
    
    async def bindEmail(
        self,
        request: UserSchema.EmailBindRequest,
        authorization: Annotated[str | None, Header()] = '',
        db: Session = Depends(GetDb)):
        try:
            emailAccount, captcha = request.emailAccount, request.captcha
            if not CheckUtil.checkEmailFormat(emailAccount):
                return CommonUtil.errorResult('不合法的邮箱地址')
            
            cacheCaptcha = redisCaptchaConn.get(f'captcha:{emailAccount}').decode('utf-8')
            if not cacheCaptcha:
                return CommonUtil.errorResult('验证码已过期，请重新获取')
            if captcha != cacheCaptcha:
                return CommonUtil.errorResult('输入的验证码不正确')
            
            userAccount = TokenUtil.getUsernameByToken(authorization.split(' ')[-1])
            loginUser = self.getUser(db, userAccount)
            if loginUser.email != '' and emailAccount == loginUser.email:
                return CommonUtil.errorResult('该账号已绑定此邮箱,请更换新的邮箱！')

            emailCountQuery = db.query(UserORM).filter_by(email=emailAccount, isDelete=0).count()
            if emailCountQuery > 0:
                return CommonUtil.errorResult('此邮箱已被绑定,请更换新的邮箱！')
            
            user = db.query(UserORM).get(loginUser.id)
            user.email = emailAccount
            db.commit()
            redisCaptchaConn.delete(f'captcha:{emailAccount}')
            return CommonUtil.successResult(data={'emailAccount': emailAccount})
        except Exception as e:
            print(f'error happen: {e}', flush=True)
            db.rollback()
            return CommonUtil.errorResult(msg=f'操作失败：{e}')
        