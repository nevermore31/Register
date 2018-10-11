import execjs
import os


class AesJs(object):
    def __init__(self, key=None, iv=None):
        '''
        :param key:  密匙
        :param iv:   位移
        '''
        self.file = './aes/AES.js'

    def js_aesencrypt(self, text, **kwargs):
        if not os.path.exists(self.file):
            self.file = './AES.js'
        f = open(self.file, 'r', encoding='utf-8').read()
        # 加密结果
        aesencrypt = execjs.compile(f).call('aesEncrypt', kwargs['key'], kwargs['iv'], text)
        return aesencrypt

    def js_gethl(self, text):
        if not os.path.exists(self.file):
            self.file = './AES.js'
        f = open(self.file, 'r', encoding='utf-8').read()

        # 相关参数
        gethl = execjs.compile(f).call('getHL', text)
        return gethl