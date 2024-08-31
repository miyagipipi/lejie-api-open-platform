from typing import Union
import jwt
from datetime import datetime, timedelta, timezone
from config.JwtConfig import SECRET_KEY, ALGORITHM, PWD_CONTEXT


def verifyPassword(plain_password, hashed_password):
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def getPasswordHash(password) -> str:
    return PWD_CONTEXT.hash(password)


def creatAccessToken(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def getUsernameByToken(token) -> str:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload.get('sub', '')
