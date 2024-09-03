from typing import TypedDict
from schema.UserSchema import UserRegistr
import re
from config.EmailConfig import EMAIL_REGEX


class baseResult(TypedDict):
    msg: str
    ret: int

def checkUserRegister(request: UserRegistr) -> baseResult:
    result = {'msg': 'success', 'ret': 0}
    if not all([request.userAccount, request.username, request.userPassword, request.checkPassword]):
        result['msg'], result['ret'] = f'账号或密码不能为空', 1
    elif len(request.userAccount) < 4:
        result['msg'], result['ret'] = '账号长度过短（至少4位）', 1
    elif len(request.userPassword) < 8 or len(request.checkPassword) < 8:
        result['msg'], result['ret'] = '账号密码过短（至少8位）', 1
    elif request.userPassword != request.checkPassword:
        result['msg'], result['ret'] = '两次输入的密码不一致', 1
    return result


def checkEmailFormat(email: str) -> bool:
    return True if re.match(EMAIL_REGEX, email) else False
