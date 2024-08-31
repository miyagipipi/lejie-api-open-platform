import redis

host = 'localhost'
port = 6379

class connectionPool():
    def __init__(self, db: int = 0) -> None:
        self.pool = redis.ConnectionPool(host=host, port=port, db=db)
    
    def getClinet(self):
        return redis.StrictRedis(connection_pool=self.pool)

redis_pool = connectionPool()
redis_job_pool = connectionPool(1)

def createClinet():
    return redis_pool.getClinet()


def createJobClient():
    return redis_job_pool.getClinet()
