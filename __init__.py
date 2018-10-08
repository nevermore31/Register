from Crypto.Cipher import AES
from Crypto import Random
import base64


# 定义 padding 即 填充 为PKCS7
def pad(s):
    while len(s) % 16 != 0:
        s += '\0'
    return str.encode(s)


def unpad(s): 
    return s[0:-ord(s[-1])]


BLOCK_SIZE = 32


class PrPcrypt(object):
    def __init__(self, key, iv=None):
        self.key = key[:32]
        # self.iv = '1234577290ABCDEF1264147890ACAE45'[:32]
        self.iv = Random.new().read(AES.block_size)
        print(self.iv)
        self.mode = AES.MODE_CBC

    def encrypt(self, text):
        text = pad(text)
        cryptor = AES.new(self.key.encode('utf-8'), self.mode, self.iv)
        self.ciphertext = cryptor.encrypt(text)
        return base64.standard_b64encode(self.ciphertext).decode("utf-8")

    def decrypt(self, text):
        cryptor = AES.new(self.key.encode('utf-8'), self.mode, self.iv)
        de_text = base64.standard_b64decode(text)
        plain_text = cryptor.decrypt(de_text)
        st = str(plain_text.decode("utf-8")).rstrip('\0')
        # out = unpad(st)
        return st


pc = PrPcrypt('c55d6db69455165598d85fb5bff9ae52', '1234577290ABCDEF1264147890ACAE45')  # 自己设定的密钥
e = pc.encrypt("123123")  # 加密内容
d = pc.decrypt(e)
print("加密后%s,解密后%s" % (e, d))