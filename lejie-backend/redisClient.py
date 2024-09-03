import redis
from config import BaseConfig


class RedisConnectionPool():
    def __init__(self, db=0):
        self.pool = redis.ConnectionPool(host=BaseConfig.REDIS_HOST, port=BaseConfig.REDIS_PORT, db=db)

    def getClient(self):
        return redis.StrictRedis(connection_pool=self.pool)


redis_job_pool = RedisConnectionPool(4) # 用于缓存定时任务
redis_captcha_pool = RedisConnectionPool() # 用于缓存邮箱验证码


def createRedisJobClient():
    return redis_job_pool.getClient()


def createRedisCaptchaClient():
    return redis_captcha_pool.getClient()
