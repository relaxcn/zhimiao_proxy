import requests
from config import baseUrl, hospitalId, cookie, proxies
from model.head import getHeader
import logging

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s-%(funcName)s',
    level=logging.INFO)


# 返回json格式
def getProductList():
    url = baseUrl
    act = "CustomerProduct"
    Hid = hospitalId
    params = {'act': act, 'id': Hid}
    head = getHeader()
    count = 3
    while count > 0:
        try:
            res = requests.get(url, params=params, headers=head, timeout=5, cookies=cookie, proxies=proxies)
        except Exception as e:
            logging.error("超时，正在重试")
            logging.error(e)
            count -= 1
        else:
            logging.info("获取商品列表成功！")
            return res.json()
    logging.error("连接失败！")
    exit(-1)


if __name__ == "__main__":
    print(getProductList())
