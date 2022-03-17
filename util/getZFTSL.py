import hashlib
import time


def getzftsl():
    _time = str(int(time.time()) - 5)
    # print(_time)
    _md5_str = "zfsw_" + _time[:-1]
    m = hashlib.md5(_md5_str.encode("utf-8"))
    # print("zftsl: "+m.hexdigest())
    return m.hexdigest()


if __name__ == '__main__':
    zftsl = getzftsl()
    print(zftsl)
