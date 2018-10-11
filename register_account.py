import random
import time
import requests
import re
import json
import csv
import os

from requests.exceptions import HTTPError
from requests.utils import dict_from_cookiejar
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
            'Cookie': 'wd_in_hy=5ba5bacf1fc166.19814741; FO_USER=dadaada223232; 51uids=453996290%2C453808427%7C264b8918'
                      'b6b43f110ac4eb4417afd4cb; FO_TUID=qRrxZm; PHPSESSID=a6r0noh0mk2ocmvgs3lcdjfb95; 5bbe05e29b8e5=15'
                      '39180261_4ed45a9cd181d1193404c7c27a758808; s_454050493=454050493%7Cdadadadada11111%7C2018-10-10+'
                      '23%3A18%3A10%7Cport_wdhy; FO_JSONP_TOKEN=da113af13e02c3976d66cc391ae62396; FO_JSONP_TIME=1539186'
                      '263; s_454050618=454050618%7Cwixiw123%7C2018-10-10+23%3A44%3A24%7Cport_wdhy; 5bbe13f2b2de3=15391'
                      '86265_98dfa2c8a83ac72118d0d6faadcd9c5f; FO_USER=wixiw123; FO_RFLP=aHR0cDovL21pY3JvLjUxLmNvbS9jbG'
                      'llbnQvaW5kZXgvaHkvP2Zyb209d2RoeSZzaXRlX2Nzcz0%3D%7CaHR0cDovL21pY3JvLjUxLmNvbS9jbGllbnQvaW5kZXgva'
                      'HkvP2Zyb209d2RoeSZzaXRlX2Nzcz0%3D%7C%7C%7C; 5bbe1e7db15d9=1539186605_c844585d683f184d9418be2b235'
                      'ba3fe; _nei_from=port_wdhy'
}


class Register(object):
    def __init__(self):
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
        req = self.s.get(start_url, headers=headers_key_iv)
        cookies = dict_from_cookiejar(req.cookies)
        if req.status_code != 200:
            raise HTTPError
        soup = BeautifulSoup(req.text, 'lxml')
        data = soup.head.find_all('script')[-1]

        # 提取key
        key_index = str(data).index('10,10')
        key = str(data)[key_index + 7:key_index + 39]

        self.validator(key)

        # 提取iv
        iv_index = str(data).index('iv')
        iv = str(data)[iv_index - 33:iv_index - 1]
        self.validator(iv)

        # 保存第一次访问的关键信息
        item = {'key': key, 'iv': iv, 'cookies': cookies}
        return item

    def _get_time(self):
        _ = str(time.time()).replace('.', '')
        return _[:13]

    def regist_for_account(self):
        # 获取 key iv cookies 值
        data = self.get_key_iv()

        # 随机生成一个账号,密码
        account = generrator_account()

        # 查看API账号是否存在
        url = 'http://passport.51.com/reg/checkusernameapi'
        data_ = {
            'chn': 'game',
            'user': str(account)
        }
        req = self.s.post(url=url, headers=self.headers_account, data=data_)
        if req.status_code == 200:
            respons = json.loads(req.text)
            if respons['ret'] != 1:
                # 不成功返回账号
                time.sleep(2)
                self.regist_for_account()

        pass_ = generrator_pass()

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
        req = self.s.get(url, headers=headers_regist, params=url_params)
        if req.status_code == 200:
            index_req = req.text.index('{')
            req_dict = json.loads(req.text[index_req:-2])
            if 'ret' in req_dict.keys():
                # 如果注册成功直接返回账号密码
                if req_dict['ret'] == 1:
                    msg_account = {'account': account, 'password': pass_,}
                    return msg_account
                # 不成功再次调用自己
                else:
                    time.sleep(2)
                    self.regist_for_account()


def write_to_csv(**kwargs):
    """
    :param kwargs: account, 账号 ， password 密码， proxies ip 地址（可能没有）
    :return:
    """
    row = [kwargs['account'], kwargs['password'],time.strftime('%Y-%m-%d %H:%M:%S')]
    if 'proxies' in kwargs.keys():
        row.insert(2, kwargs['proxies'])
    if os.path.exists('./账号文件夹/')is False:
        os.makedirs('./账号文件夹/')
    with open('./账号文件夹/account.csv', 'a+')as f:
        write = csv.writer(f)
        write.writerow(row)


def main(**kwargs):
    """
    注册账号，将信息保存csv文档中
    # 后期添加代理后可以添加多线程
    :param count: 程序启动注册多少个账号
    :return: NONE
    """
    if kwargs['count'] is None:
        count = 1
    else: count = kwargs['count']
    for c_ in range(count):
        register = Register().regist_for_account()
        write_to_csv(account=register['account'], password=register['password'])


