import requests
import time

if __name__ == '__main__':
    url = "https://www.taobao.com/help/getip.php"
    head = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
    }

    proxies = {
        "http": "tps584.kdlapi.com:15818",
        "https": "tps584.kdlapi.com:15818"
    }
    while True:
        res = requests.get(url, headers=head, proxies=proxies)
        time.sleep(0.3)
        print(res.text)