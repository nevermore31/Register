import random
import time
import requests
import re
import pprint
import json

from requests.exceptions import HTTPError
from requests.utils import dict_from_cookiejar
from bs4 import BeautifulSoup
from user_agent import user_agent
from aes import AesJs
from account_generator import generrator_pass, generrator_account


agent = random.choice(user_agent)
# 注册页面请求头
headers_regist = {
    'Connection': 'keep-alive',
    'Cookie': 'FO_RFLP=aHR0cDovL21pY3JvLjUxLmNvbS9jbGllbnQvaW5kZXgvaHkvP2Zyb209d2RoeSZzaXRlX2Nzcz0%3D%7CaHR0cDo'
              'vL21pY3JvLjUxLmNvbS9jbGllbnQvcmVnL2h5Lz9mcm9tPXdkaHkmc2l0ZV9jc3M9%7C%7C%7C; FO_TUID=sN1hfZ; '
              'PHPSESSID=sducvqmjirc9gorbsncqf30l35; _nei_from=port_wdhy; wd_in_hy=5bbd647d9a54b9.40824442; FO_'
              'JSONP_TOKEN=e1b04dc7f2a66e1467934304128dae54; FO_JSONP_TIME={}; 5bbd5d2273cca=1539139004'
              '_8d94e2a9acb4f7831074a9fcbe72a5c8'.format(int(time.time())),
    'Host': 'passport.51.com',
    'Referer': 'http://micro.51.com/client/reg/hy/?from=wdhy&site_css=',
    'User-Agent': agent}

# 获取key iv 请求头
headers_key_iv = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Cookie': 'FO_RFLP=aHR0cDovL21pY3JvLjUxLmNvbS9jbGllbnQvaW5kZXgvaHkvP2Zyb209d2RoeSZzaXRlX2Nzcz0%3D%7CaHR0cDo'
                      'vL21pY3JvLjUxLmNvbS9jbGllbnQvcmVnL2h5Lz9mcm9tPXdkaHkmc2l0ZV9jc3M9%7C%7C%7C; FO_TUID=sN1hfZ; '
                      'PHPSESSID=sducvqmjirc9gorbsncqf30l35; _nei_from=port_wdhy; wd_in_hy=5bbd647d9a54b9.40824442; FO_'
                      'JSONP_TOKEN=e1b04dc7f2a66e1467934304128dae54; FO_JSONP_TIME={}; 5bbd5d2273cca=1539139004'
                      '_8d94e2a9acb4f7831074a9fcbe72a5c8'.format(int(time.time())),
            'Host': 'micro.51.com',
            'Referer': 'http://micro.51.com/client/index/hy/?from=wdhy&site_css=',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': agent
        }
# 请勿改动，否则无法访问该接口
headers_account = {
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Cookie': 'FO_RFLP=aHR0cDovL21pY3JvLjUxLmNvbS9jbGllbnQvaW5kZXgvaHkvP2Zyb209d2RoeSZzaXRlX2Nzcz0%3D%7CaHR0cDo'
                      'vL21pY3JvLjUxLmNvbS9jbGllbnQvcmVnL2h5Lz9mcm9tPXdkaHkmc2l0ZV9jc3M9%7C%7C%7C; FO_TUID=sN1hfZ; '
                      'PHPSESSID=sducvqmjirc9gorbsncqf30l35; _nei_from=port_wdhy; wd_in_hy=5bbd647d9a54b9.40824442; FO_'
                      'JSONP_TOKEN=e1b04dc7f2a66e1467934304128dae54; FO_JSONP_TIME={}; 5bbd5d2273cca=1539139004'
                      '_8d94e2a9acb4f7831074a9fcbe72a5c8'.format(int(time.time())),
            'Host': 'passport.51.com',
            'Origin': 'http://passport.51.com',
            'Referer': 'http://passport.51.com/login/proxy',
            'User-Agent': agent
        }


class Register(object):
    def __init__(self):
        self.session = requests.Session()
        self.headers_regist = headers_regist
        self.headers_key_iv = headers_key_iv
        self.headers_account = headers_account
        self.aes = AesJs()

    def validator(self, s):
        if len(s) != 32:
            raise TypeError
        elif re.match('[a-zA-Z]', s) is False:
            raise TypeError
        elif re.match('[0-9]', s) is False:
            raise TypeError
        return s

    def get_key_iv(self):
        start_url = 'http://micro.51.com/client/reg/hy/?from=wdhy&site_css='
        req = self.session.get(start_url)
        if req.status_code != 200:
            raise HTTPError
        soup = BeautifulSoup(req.text, 'lxml')
        data = soup.head.find_all('script')[-1]

        # 提取key
        key_index = str(data).index('key')
        key = str(data)[key_index + 6:key_index + 38]
        self.validator(key)

        # 提取iv
        iv_index = str(data).index('iv')
        iv = str(data)[iv_index - 33:iv_index - 1]
        self.validator(iv)
        item = {'key': key, 'iv': iv}
        return item

    def _get_time(self):
        _ = str(time.time()).replace('.', '')
        return _[:13]

    def regist_for_account(self):
        # 获取 key iv值
        data = self.get_key_iv()
        print(data)

        # 随机生成一个账号,密码
        account = generrator_account()

        # 查看API账号是否存在
        url = 'http://passport.51.com/reg/checkusernameapi'
        data_ = {
            'chn': 'game',
            'user': str(account)
        }
        req = self.session.post(url=url, headers=self.headers_account, data=data_)
        if req.status_code == 200:
            respons = json.loads(req.text)
            print(respons)
            if respons['ret'] != 1:
                # 不成功返回账号
                time.sleep(2)
                self.regist_for_account()

        pass_ = generrator_pass()
        msg_account = {'account': account, 'password': pass_}

        user = self.aes.js_aesencrypt(text=account, key=data['key'], iv=data['iv'])
        password = self.aes.js_aesencrypt(text=pass_, key=data['key'], iv=data['iv'])

        user_ht = self.aes.js_gethl(account)
        password_ht = self.aes.js_gethl(pass_)

        # 注册账号请求信息
        url_querty = {
            'callback': 'jQuery111102791574350174819_{}'.format(self._get_time()),
            'chn': 'game',
            'type': 'username',
            'user': user,
            'pass': password,
            'repass': password,
            'sex': '1',
            'from': 'wdhy',
            'reg_url': 'http%3A%2F%2Fmicro.51.com%2Fclient%2Freg%2Fhy%2F%3Ffrom%3Dwdhy%26site_css%3D%23%23%23',
            'referer_url': 'http%3A%2F%2Fmicro.51.com%2Fclient%2Findex%2Fhy%2F%3Ffrom%3Dwdhy%26site_css%3D',
            'redirect_url': 'http%3A%2F%2Fmicro.51.com%2Fclient%2Findex%2Fhy%2F%3Ffrom%3Dwdhy%26site_css%3D',
            'isAutoLogin': '1',
            'aes': '1',
            'user_ht': user_ht,
            'password_ht': password_ht,
            'repassword_ht': password_ht,
            '_': self._get_time()
        }
        pprint.pprint(url_querty)

        # 构造url， 进行注册请求
        url = 'https://passport.51.com/reg/qJsonpApi?'
        for u in url_querty.items():
            url += u[0]+'='+u[1]+'&'
        print(url)
        req = self.session.get(url, headers=headers_regist)
        if req.status_code == 200:
            print(req.text)
            print(msg_account)


if __name__ == '__main__':
    Register().regist_for_account()