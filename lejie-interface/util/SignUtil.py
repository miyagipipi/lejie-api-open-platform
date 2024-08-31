import hashlib


def genSign(body: str, secretKey: str) -> str:
    sha256_hash = hashlib.sha256()
    content = f'{body}.{secretKey}'
    sha256_hash.update(content.encode('utf-8'))
    return sha256_hash.hexdigest()