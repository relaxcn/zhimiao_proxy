from util.person import getUserInfo
from config import productID
from util.crypt import encrypt
import logging
logging.basicConfig(
                     format = '%(asctime)s - %(levelname)s - %(message)s-%(funcName)s',
                     level=logging.INFO)


# 传入解密之后得到的 mxid， 得到字符串明文
def getOrderPostInfo(mxid, userInfo, date):

    postInfo = {
        "birthday": userInfo['birthday'],
        "tel": userInfo['tel'],
        "sex": userInfo['sex'],
        "cname": userInfo['cname'],
        "doctype": userInfo['doctype'],
        "idcard": userInfo['idcard'],
        "mxid": mxid,
        "date": date,
        "pid": productID,
        "Ftime": 1,
        "guid": ""
    }
    _postInfo = str(postInfo).replace("'", '"')
    __postInfo = _postInfo.replace(" ", '')
    return __postInfo

# 得到加密后的密文 用于Post
# 参数： mxid
def getOrderPostInfoEncrypted(mxid, userInfo, date):
    plaintext = getOrderPostInfo(mxid, userInfo, date)
    logging.info("加密前：" + plaintext)
    encrypted_str = encrypt(plaintext)
    return encrypted_str


if __name__ == '__main__':
    userInfo = getUserInfo()
    print(getOrderPostInfo("ZGquAA-lAAA5iTQB"))
    print(getOrderPostInfoEncrypted("ZGquAA-lAAA5iTQB"))
