from getProductList import getProductList
from getZFTSL import getzftsl
from order import getMxid
from person import flash

if __name__ == "__main__":
    flash()
    print("getzftsl------------")
    print(getzftsl())
    print("getProductList---------")
    print(getProductList())
    print(getMxid())
