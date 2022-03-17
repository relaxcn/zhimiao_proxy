from config import cookie, user_agent, Referer
from util.getZFTSL import getzftsl


def getHeader():
    head = {
        "Host": "cloud.cn2030.com",
        # "Connection": "keep-alive",
        "User-Agent": user_agent,
        "content-type": "application/json",
        "zftsl": getzftsl(),
        "Referer": Referer
    }
    return head
