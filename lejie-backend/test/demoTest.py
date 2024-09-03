import random, string


def genRandomUserAccount(length):
    letters = string.ascii_letters  # 包含所有大小写字母
    return ''.join(random.choice(letters) for i in range(length))

# 生成一个长度为10的随机字符串
random_string = genRandomUserAccount(12)
print(random_string)