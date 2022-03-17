import base64
import json
from config import cookie


def deCryptKey(cookie_value):
    arr = cookie_value.split(".")
    # head_str = base64.b64decode(arr[0])
    arr1 = arr[1]
    if len(arr1) % 4:
        arr1 += '=' * (4 - len(arr1) % 4)

    payload_str = base64.b64decode(arr1)
    val = json.loads(payload_str.decode('utf-8'))['val']

    sign_key = base64.b64decode(val)[9:25].decode('utf-8')
    # print(arr)
    # print(head_str)
    # print(payload_str)
    # print(val)
    return str(sign_key)


# 根据Cookie解密出sign_key str
def getSign():
    cookie_value = cookie['ASP.NET_SessionId']
    key = deCryptKey(cookie_value)
    return key


if __name__ == '__main__':
    key = getSign()
    print(key.encode('utf-8'), len(key))
