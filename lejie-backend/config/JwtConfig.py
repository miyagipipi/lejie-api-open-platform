from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer


SECRET_KEY = '3e6d15c08277329d5f30ce830b57b1a150a9da1619058067e14b16ef8ce20374'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440
PWD_CONTEXT = CryptContext(schemes=['bcrypt'], deprecated='auto')
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl='/user/token')
