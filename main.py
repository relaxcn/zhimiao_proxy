import time
import logging
import schedule
import threading
import requests.exceptions
from config import cookie, curdate
from util.order import getMxid, GetCaptcha, GetOrderStatus, OrderPost, getOrderPostInfoEncrypted
from util.person import getUserInfo, flash, GetCustSubscribeDateAll
import logging

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s-%(funcName)s',
    level=logging.INFO)


def loopGetMxid(date):
    try:
        mxid = getMxid(date)
        while not mxid:
            logging.error("获取mxid失败，抢购尚未开始，正在重试")
            mxid = getMxid(date)
    # 遇到错误，remote close,返回 False
    except requests.exceptions.ConnectionError as e:
        logging.error(e)
        return False
    else:
        logging.info("得到Mxid")
        return mxid


def run():
    logging.info("开始")
    userInfo = getUserInfo()

    logging.info(userInfo)
    if not userInfo:
        logging.error("获取用户信息失败，请检查Cookie")
        exit(-1)

    # 指定日期
    if curdate != "null":
        # 指定单个日期
        DateList = [{'date': curdate, 'enable': True}]

        logging.info("指定的日期列表：" + str(DateList))

        logging.info("=======正在进行尝试。。。")
        # 指定日期预约
        try:
            logging.info("==========尝试指定日期: " + curdate)
            if curdate not in str(DateList):
                logging.info("指定日期不在预约日期列表，进行顺序预约")
            else:
                start = str(DateList).find(curdate) + 23
                end = str(DateList).find("}", start)
                isOk = str(DateList)[start: end]
                # 查看指定日期是否已满
                if isOk == "True":
                    # 使用指定日期获取mxid
                    try:
                        logging.info("使用date: " + curdate + "获取mxid")
                        mxid = loopGetMxid(date=curdate)
                    except IndexError as e:
                        logging.error(e)
                        logging.error("获取mxid失败")
                    # 获取成功之后
                    else:
                        if not mxid:
                            logging.error("remote close!")
                            exit(-1)
                        # check mxid
                        logging.info("checking ....")
                        new_cookie = GetCaptcha(mxid)
                        # 构造post form
                        post_data = getOrderPostInfoEncrypted(mxid, userInfo, date=curdate)
                        logging.info("加密后密文: " + post_data)

                        new_new_cookie = OrderPost(new_cookie, post_data)
                        # 如果提交成功，返回200
                        if new_new_cookie is not False:


                            last_cookie, info = GetOrderStatus(new_new_cookie)
                            if "200" in info:
                                logging.info("预约成功！")
                                exit(0)
                            elif "300" in info:
                                logging.info("该身份证或微信号已有预约信息")
                                exit(0)
                            elif "201" in info:
                                logging.info("日期错误")
                                exit(-1)
                            else:
                                logging.error("失败！")
                        else:
                            logging.error("Order Post 返回False")
                else:
                    logging.error("指定日期已满")
        except Exception as e:
            logging.error("指定日期失败！")
            logging.error(e)

    # 获取所有日期 list
    DateList = GetCustSubscribeDateAll()
    while DateList is False:
        logging.error("获取所有接种日期失败，时间还未开始")
        DateList = GetCustSubscribeDateAll()
    logging.info("获取到接种日期列表：" + str(DateList))

    try:
        # 顺序预约
        for timedate in DateList:
            # 获取到时间
            date = timedate['date']
            # 指定日期失败的，则直接跳过
            if date == curdate:
                continue
            # 如果不可预约则直接break
            logging.info("==========尝试接种日期： " + date)
            if timedate['enable'] is False:
                logging.error("已满!")
                continue
            # 如果可以预约，获取mxid
            try:
                logging.info("使用date: " + date + "获取mxid")
                mxid = loopGetMxid(date=date)
            except IndexError as e:
                logging.error(e)
                logging.error("获取mxid失败")
                continue
            if not mxid:
                logging.error("remote close failed!")
                exit(-1)
            # check mxid
            logging.info("checking ....")
            new_cookie = GetCaptcha(mxid)
            # 构造post form
            post_data = getOrderPostInfoEncrypted(mxid, userInfo, date=date)
            logging.info("加密后密文: " + post_data)

            # 提交订单
            new_new_cookie = OrderPost(new_cookie, post_data)
            # 如果返回False，证明已满或者其他原因
            if new_new_cookie is False:
                continue
            last_cookie, info = GetOrderStatus(new_new_cookie)
            if "200" in info:
                logging.info("预约成功！")
                exit(0)
            elif "300" in info:
                logging.info("该身份证或微信号已有预约信息")
                exit(0)
            elif "201" in info:
                logging.info("日期错误")
            else:
                continue

        logging.error("失败！所有日期都满!")
        exit(-1)
    except Exception as e:
        logging.error(e)
        logging.error("顺序预约遇到异常，退出！")
        exit(-1)


def delayRun():
    logging.info("dalayRun.........")
    time.sleep(57.5)
    logging.info("Start Run.........")
    run()


def timeRun(time):
    # 09:59
    schedule.every().day.at(time).do(delayRun)
    while True:
        schedule.run_pending()

def threadRun(count):
    logging.info("All thread start")
    try:
        threadSet = []
        for i in range(count):
            logging.warning("i = " + str(i))
            thread = threading.Thread(target=run)
            threadSet.append(thread)
        for thread in threadSet:
            thread.start()
        for thread in threadSet:
            thread.join()
    except Exception as e:
        print("---------")
        print(e)
        print("---------")
        logging.error("Error:无法创建线程")
    logging.info("All thread END!")



if __name__ == '__main__':
    # run()
    schedule.every().day.at("16:54").do(threadRun, 7)
    while True:
        schedule.run_pending()
