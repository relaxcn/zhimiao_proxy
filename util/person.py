import logging

from config import baseUrl, productID, hospitalId, month, cookie, userInfo, proxies, timeout
from util.getProductList import getProductList
from model.head import getHeader
import requests
from util.crypt import decrypt
import re
import json
logging.basicConfig(
                     format = '%(asctime)s - %(levelname)s - %(message)s-%(funcName)s',
                     level=logging.INFO)


# 获取个人信息
# return a dict or False
def getUserInfo(isFlash=False):
    if isFlash:
        logging.info("getUserInfo....")
        act = "User"
        params = {"act": act}
        head = getHeader()

        count = 3
        while count > 0:
            try:
                res = requests.get(baseUrl, headers=head, params=params, cookies=cookie, timeout=timeout, proxies=proxies).json()
            except Exception as e:
                logging.error("超时，正在重试")
                logging.error(e)
                count -= 1
            else:
                if res['status'] == 200:
                    return res['user']
                logging.error("Cookie失效")
                return False
        logging.error("连接失败！")
        exit(-1)
    else:
        # 节省带宽，从配置文件中直接获取
        js = json.loads(userInfo.replace("'", '"'))
        return js


# 获取指定医院和商品的接种日期
# return a list or False
def GetCustSubscribeDateAll():
    params = {
        "act": "GetCustSubscribeDateAll",
        "pid": productID,
        "id": hospitalId,
        "month": month
    }
    head = getHeader()

    count = 3
    while count > 0:
        try:
            res = requests.get(baseUrl, headers=head, params=params, cookies=cookie, proxies=proxies, timeout=timeout).json()
        except Exception as e:
            logging.error("超时，正在重试")
            logging.error(e)
            count -= 1
        else:
            if res['status'] == 200:
                if 'list' in str(res):
                    return res['list']
            logging.error(res)
            return False
    logging.error("连接失败！")
    exit(-1)


# 查询详细接种日期
# 传入一个指定日期的字符串，例如'2022-2-17'，使用函数GetCustSubscribeDateAll获得
# 返回未解密的字符串
def GetCustSubscribeDateDetail(scdate):
    params = {
        "act": "GetCustSubscribeDateDetail",
        "pid": productID,
        "id": hospitalId,
        "scdate": scdate
    }
    head = getHeader()
    logging.info(params)

    count = 3
    while count > 0:
        try:
            res = requests.get(baseUrl, headers=head, params=params, cookies=cookie, proxies=proxies, timeout=timeout)
        except Exception as e:
            logging.error("超时，正在重试")
            logging.error(e)
            count -= 1
        else:
            # 如果返回不正确信息
            if 'list' in res.text or '<!DOCTYPE html>' in res.text:
                if '<!DOCTYPE html>' in res.text:
                    logging.error("得到错误服务器返回信息！<!DOCTYPE html>")
                if 'list' in res.text:
                    logging.info("未查询到详细接种日期，或者还未开始抢购" + res.text)
                return False
            logging.info("接收到密文: " + res.text)
            return res.text
    logging.error("连接失败！")
    exit(-1)


# 刷新
def flash():
    isSuccess = False
    while isSuccess is not True:
        try:
            getUserInfo(True)
            print(getProductList())
            GetCustSubscribeDateAll()
            GetCustSubscribeDateDetail("2022-03-05")
        except Exception as e:
            logging.error(e)
            logging.error("flash failed")
            isSuccess = False
        else:
            isSuccess = True


# 返回解密后的数据 查询详细接种时间段
# 参数：Str
def getDetailDateFromDecrypt(scdate):
    ciphertext = GetCustSubscribeDateDetail(scdate)
    if ciphertext is False:
        return False
    text = decrypt(ciphertext)
    if text is False:
        return False
    _text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', text)
    return _text


if __name__ == "__main__":
    flash()
    # print(getUserInfo(True))
    # getProductList()
    # print(GetCustSubscribeDateAll())
    # # print(GetCustSubscribeDateDetail("2022-02-15"))
    # print(getDetailDateFromDecrypt("2022-02-28"))
