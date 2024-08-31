import requests
import random, time
from . import Config
import hashlib


__version__ = "0.0.1"
__title__ = "PyLejieClientSDK"
__author__ = "miyagipipi"



def genSign(body: str, secretKey: str) -> str:
    sha256_hash = hashlib.sha256()
    content = f'{body}.{secretKey}'
    sha256_hash.update(content.encode('utf-8'))
    return sha256_hash.hexdigest()

class LejieApiClient():
    def __init__(self, accessKey: str, secretKey: str, host: str, port: int) -> None:
        self.url = f'http://{host}:{port}'
        self.accessKey = accessKey
        self.secretKey = secretKey
    
    def unifyHeaders(self, body: str):
        result = {
            'body': body,
            'accessKey': self.accessKey,
            'nonce': str(random.randint(0, 100)),
            'timestamp': str(int(time.time())),
        }
        result['sign'] = genSign(body, self.secretKey)
        return result
    
    def getNameByGet(self, name: str):
        payload = {'name': name}
        r = requests.get(f"{self.url}/api/name/", params=payload)
        return r.text

    def getNameByPost(self, name: str):
        payload = {'name': name}
        r = requests.post(url=f"{self.url}/api/name/", json=payload)
        return r.text

    def getUsernameByPost(self, userAccount: str):
        try:
            r = requests.post(
                url=f"{self.url}/api/name/user",
                json={'userAccount': userAccount},
                headers=self.unifyHeaders(userAccount))
            return r.text
        except requests.exceptions.HTTPError as err:
            return err.response.text  # 或者根据需要返回其他内容

__all__ = [
    "LejieApiClient"
]
