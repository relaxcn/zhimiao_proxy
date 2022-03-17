from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from config import iv
import logging
from util.getSign import getSign
logging.basicConfig(
                     format = '%(asctime)s - %(levelname)s - %(message)s-%(funcName)s',
                     level=logging.INFO)

# 解密
# 参数：密文
def decrypt(ciphertext):
    key = getSign()
    logging.info("key = " + key)
    b_text = bytes.fromhex(ciphertext)
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
    try:
        plaintext = cipher.decrypt(b_text).decode('utf-8')
    except UnicodeDecodeError as e:
        logging.error(e)
        logging.error("key = " + key)
        logging.error("key已经失效，请重新获取")
        exit(-1)
    else:
        return plaintext


# 加密 参数：明文
def encrypt(plaintext: str):
    key = getSign()
    logging.info("key = " + key)
    cipher = AES.new(key.encode("utf-8"), AES.MODE_CBC, iv.encode('utf-8'))
    pad_pkcs7 = pad(plaintext.encode('utf-8'), AES.block_size, style="pkcs7")
    ciphertext = bytes.hex(cipher.encrypt(pad_pkcs7))
    return ciphertext


if __name__ == '__main__':
    plaintext_str = '{"birthday":"2000-12-07","tel":"15225995820","sex":2,"cname":"陈帅","doctype":1,"idcard":"411729200012072111","mxid":"ZGquAA-lAAA5iTQB","date":"2022-02-17","pid":"54","Ftime":1,"guid":""}'
    en_str = encrypt(plaintext_str)
    de_str = decrypt(en_str)
    print(en_str)
    print(de_str.encode('utf-8'))
