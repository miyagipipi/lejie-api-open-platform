from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DatabaseConfig
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

base_url = "{0}:{1}@{2}:{3}/{4}".format(
    DatabaseConfig.user,
    DatabaseConfig.pwd,
    DatabaseConfig.host,
    DatabaseConfig.port,
    DatabaseConfig.name
)

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://{0}".format(base_url)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def GetDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def GetSession():
    return SessionLocal()

"""
异步的数据库会话
"""
SQLALCHEMY_ASYNC_DATABASE_URL = "mysql+aiomysql://{0}".format(base_url)
async_engine = create_async_engine(SQLALCHEMY_ASYNC_DATABASE_URL)
AsyncSessionLocal = sessionmaker(
    bind=async_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)
async def GetAsyncDB():
    async with AsyncSessionLocal() as session:
        yield session

