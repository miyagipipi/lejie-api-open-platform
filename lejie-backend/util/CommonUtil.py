import random, string


def randomNumbers(n: int) -> int:
    if n == 0:
        return 0
    minVal = 10**(abs(n) - 1)
    maxVal = (10**abs(n)) - 1
    
    return random.randint(minVal, maxVal)


def genRandomUserAccount(length: int) -> str:
    letters = string.ascii_letters  # 包含所有大小写字母
    return ''.join(random.choice(letters) for i in range(length))


def errorResult(msg='error', data={}):
    return {'ret': 1, 'msg': msg, 'data': data}


def successResult(msg='success', data={}):
    return {'ret': 0, 'msg': msg, 'data': data}
