from typing import TypedDict


class baseResult(TypedDict):
    msg: str
    ret: int

def checkUserRegister(userAccount: str, userPassword: str, checkPassword: str) -> baseResult:
    result = {'msg': 'success', 'ret': 0}
    if not all([userAccount, userPassword, checkPassword]):
        result['msg'], result['ret'] = f'账号或密码不能为空', 1
    elif len(userAccount) < 4:
        result['msg'], result['ret'] = '账号长度过短（至少4位）', 1
    elif len(userPassword) < 8 or len(checkPassword) < 8:
        result['msg'], result['ret'] = '账号密码过短（至少8位）', 1
    elif userPassword != checkPassword:
        result['msg'], result['ret'] = '两次输入的密码不一致', 1
    return result
