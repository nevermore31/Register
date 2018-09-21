import requests
import random

from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

from UserAgent import user_agent
# account <dadssada123131>   <AR+97UfVrXeNn3C7zI4OdA==>
# password <123456>   <OtfhXpaw3RTokam4QADshA==>


class Register(object):
    def __init__(self):
        pass

    def req(self):
        # <headers> 请求
        #  GET请求.后面带参数
        url = 'https://passport.51.com/reg/qJsonpApi'
        url_querty = {
            'callback': 'jQuery111102791574350174819_1537511222705',
            'chn': 'game',
            'type': 'username',
            'user': None,
            'pass': None,
            'repass': None,
            'sex': '1',
            'from': 'wdhy',
            'reg_url': 'http%3A%2F%2Fmicro.51.com%2Fclient%2Freg%2Fhy%2F%3Ffrom%3Dwdhy%26site_css%3D%23%23%23',
            'referer_url': 'http%3A%2F%2Fmicro.51.com%2Fclient%2Findex%2Fhy%2F%3Ffrom%3Dwdhy%26site_css%3D',
            'redirect_url': 'http%3A%2F%2Fmicro.51.com%2Fclient%2Findex%2Fhy%2F%3Ffrom%3Dwdhy%26site_css%3D',
            'isAutoLogin': '1',
            'aes': '1',
            'user_ht': 'd1',
            'password_ht': '16',
            'repassword_ht': '16',
            '_': '1537511222706'
        }
        headers = {
            'Connection': 'keep-alive',
            'Cookie': 'FO_USER=hhhh131231; 51uids=453785025%7C6bb7805df8c216c054701ec24f50fed2; FO_TUID=ysIw57; PHPSESS'
                      'ID=ocb0lcn4r98jcobl357a1va041; s_453808134=453808134%7Cqqd3132131%7C2018-09-21+14%3A15%3A18%7Cpo'
                      'rt_wdhy; s_453808210=453808210%7Chhhh13123131%7C2018-09-21+14%3A20%3A28%7Cport_wdhy; s_453808216'
                      '=453808216%7Chh123123131%7C2018-09-21+14%3A21%3A13%7Cport_wdhy; s_453808278=453808278%7Cdada1234'
                      '55%7C2018-09-21+14%3A26%3A44%7Cport_wdhy; FO_RFLP=aHR0cDovL21pY3JvLjUxLmNvbS9jbGllbnQvaW5kZXgvaH'
                      'kvP2Zyb209d2RoeSZzaXRlX2Nzcz0%3D%7CaHR0cDovL21pY3JvLjUxLmNvbS9jbGllbnQvaW5kZXgvaHkvP2Zyb209d2Roe'
                      'SZzaXRlX2Nzcz0%3D%7C%7C%7C; _nei_from=port_wdhy; 5ba488e2b5e73=1537511222_d6c00a347af9de5fc00920'
                      'ce192f0ca7; FO_JSONP_TOKEN=ba4280965cf02c2d55eccb0e166b78ce; FO_JSONP_TIME=1537511245',
            'Host': 'passport.51.com',
            'Referer': 'http://micro.51.com/client/reg/hy/?from=wdhy&site_css=',
            'User-Agent': random.choice(user_agent)
        }



