
import requests
import util.person as person
from model.orderPost import getOrderPostInfoEncrypted
from model.head import getHeader
from config import baseUrl, cookie, postUrl, proxies
import json
import logging
logging.basicConfig(
                     format = '%(asctime)s - %(levelname)s - %(message)s-%(funcName)s',
                     level=logging.INFO)


def getMxid(date):
    detailDateText = person.getDetailDateFromDecrypt(scdate=date)
    if detailDateText:
        logging.info("解密后明文：" + str(detailDateText))
        detailDateJson = json.loads(detailDateText.encode("utf-8"))

        mxid = detailDateJson['list'][0]['mxid']
        logging.info("mxid: " + mxid)
        return mxid
    else:
        logging.error("获取mxid失败")
        return False


# 返回新的Cookie
def GetCaptcha(mxid):
    head = getHeader()
    params = {
        "act": "GetCaptcha",
        "mxid": mxid
    }

    count = 3
    while count > 0:
        try:
            res = requests.get(baseUrl, params=params, headers=head, cookies=cookie, allow_redirects=False, proxies=proxies)
        except Exception as e:
            logging.error("超时，正在重试")
            logging.error(e)
            count -= 1
        else:
            logging.info("GetCaptcha success")
            if res.json()['status'] == 200:
                logging.info(res.text)
                # print(res.headers)
                # print(res.cookies.get_dict())
                new_cookie = res.cookies.get_dict()
                logging.info("new cookie: " + str(new_cookie))
                return new_cookie
            else:
                return False
    logging.error("连接失败！")
    exit(-1)


# 需要加密之后的数据data和new_cookie
# 如果提交成功，返回另一个新的Cookie dict
def OrderPost(new_cookie, data):
    if data:
        head = getHeader()
        while True:
            try:
                res = requests.post(postUrl, headers=head, cookies=new_cookie, data=data, proxies=proxies)
            except requests.exceptions.Timeout as e:
                logging.error(e)
                logging.error("Order Post 超时，正在重试!")
            except requests.exceptions.ProxyError as e:
                logging.error(e)
                logging.error("Proxy 错误")
            else:
                # print(res.text)
                logging.info("order Post提交成功，返回 : "+res.text)
                if "200" in res.text:
                    # print(res.headers)
                    # print(res.cookies.get_dict())
                    new_new_cookie = res.cookies.get_dict()
                    logging.info("new_new_cookie : " + str(new_new_cookie))
                    return new_new_cookie
                else:
                    logging.error("order Post 返回:" + res.text)
                    return False

    return False


# 查询提交状态
# 返回最新Cookie 和信息Str
def GetOrderStatus(new_new_cookie):
    params = {
        "act": "GetOrderStatus"
    }
    head = getHeader()

    count = 3
    while count > 0:
        try:
            res = requests.get(baseUrl, params=params, headers=head, cookies=new_new_cookie, proxies=proxies)
        except Exception as e:
            logging.error("超时，正在重试")
            logging.error(e)
            count -= 1
        else:
            logging.info(res.text)
            last_cookie = res.cookies.get_dict()
            logging.info("last_Cookie : " + str(last_cookie))
            return last_cookie, res.text

    logging.error("连接失败！")
    exit(-1)


if __name__ == '__main__':
    userInfo = person.getUserInfo()
    mxid = getMxid(2022-3)
    # new_cookie = GetCaptcha(mxid)
    # data = getOrderPostInfoEncrypted(mxid, userInfo)
    # print("加密后密文: " + data)
    # new_new_cookie = OrderPost(new_cookie, data)
    # last_cookie, info_text = GetOrderStatus(new_new_cookie)

