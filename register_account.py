import random
import time
import requests
import re
import pprint
import json

from requests.exceptions import HTTPError
from requests.utils import dict_from_cookiejar, cookiejar_from_dict
from bs4 import BeautifulSoup
from user_agent import user_agent
from aes import AesJs
from account_generator import generrator_pass, generrator_account


agent = random.choice(user_agent)
# 注册页面请求头
headers_regist = {
    'Accept': '*/*',
    'Connection': 'keep-alive',
    'Host': 'passport.51.com',
    'Referer': 'http://micro.51.com/client/reg/hy/?from=wdhy&site_css=',
    'User-Agent': agent}

# 获取key iv 请求头
headers_key_iv = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'micro.51.com',
            'Referer': 'http://micro.51.com/client/index/hy/?from=wdhy&site_css=',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': agent,
}

# 请勿改动，否则无法访问该接口
headers_account = {
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Host': 'passport.51.com',
            'Origin': 'http://passport.51.com',
            'Referer': 'http://passport.51.com/login/proxy',
            'User-Agent': agent,
    'Cookie': 'wd_in_hy=5ba5bacf1fc166.19814741; FO_USER=dadaada223232; 51uids=453996290%2C453808427%7C264b8918b6b43f110ac4eb4417afd4cb; FO_TUID=qRrxZm; PHPSESSID=a6r0noh0mk2ocmvgs3lcdjfb95; 5bbe05e29b8e5=1539180261_4ed45a9cd181d1193404c7c27a758808; s_454050493=454050493%7Cdadadadada11111%7C2018-10-10+23%3A18%3A10%7Cport_wdhy; FO_JSONP_TOKEN=da113af13e02c3976d66cc391ae62396; FO_JSONP_TIME=1539186263; s_454050618=454050618%7Cwixiw123%7C2018-10-10+23%3A44%3A24%7Cport_wdhy; 5bbe13f2b2de3=1539186265_98dfa2c8a83ac72118d0d6faadcd9c5f; FO_USER=wixiw123; FO_RFLP=aHR0cDovL21pY3JvLjUxLmNvbS9jbGllbnQvaW5kZXgvaHkvP2Zyb209d2RoeSZzaXRlX2Nzcz0%3D%7CaHR0cDovL21pY3JvLjUxLmNvbS9jbGllbnQvaW5kZXgvaHkvP2Zyb209d2RoeSZzaXRlX2Nzcz0%3D%7C%7C%7C; 5bbe1e7db15d9=1539186605_c844585d683f184d9418be2b235ba3fe; _nei_from=port_wdhy'
}


class Register(object):
    def __init__(self):
        self.r = requests
        self.s = requests.session()
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
        req = self.r.get(start_url, headers=headers_key_iv)
        print(req.cookies)
        cookies = dict_from_cookiejar(req.cookies)
        for key in ['PHPSESSID', 'wd_in_hy']:
            del cookies[key]
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

        # 重新获取cookies 更新PHPSESSID
        req = self.r.get(start_url, headers=headers_key_iv)
        cookies_ = dict_from_cookiejar(req.cookies)
        cookies['PHPSESSID'] = cookies_['PHPSESSID']
        print(cookies_)
        # 保存第一次访问的关键信息
        item = {'key': key, 'iv': iv, 'cookies': cookies}
        return item

    def _get_time(self):
        _ = str(time.time()).replace('.', '')
        return _[:13]

    def regist_for_account(self):
        # 获取 key iv cookies 值
        data = self.get_key_iv()

        self.s.cookies = cookiejar_from_dict(data['cookies'])

        # 随机生成一个账号,密码
        account = generrator_account()

        # 查看API账号是否存在
        url = 'http://passport.51.com/reg/checkusernameapi'
        data_ = {
            'chn': 'game',
            'user': str(account)
        }
        print(self.s.cookies)
        req = self.s.post(url=url, headers=self.headers_account, data=data_)
        print(req.cookies)
        if req.status_code == 200:
            respons = json.loads(req.text)
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
        url_params = {
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
        # pprint.pprint(url_querty)

        # 构造url， 进行注册请求
        url = 'https://passport.51.com/reg/qJsonpApi'
        print(self.s.cookies)
        req = self.s.get(url, headers=headers_regist, params=url_params)
        print(req.cookies)
        if req.status_code == 200:
            print(req.text)
            # print(msg_account)


if __name__ == '__main__':
    Register().regist_for_account()