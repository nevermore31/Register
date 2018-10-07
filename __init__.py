from Crypto.Cipher import AES
import base64


BS = AES.block_size


# 定义 padding 即 填充 为PKCS7
def pad(s): 
    return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)


def unpad(s): 
    return s[0:-ord(s[-1])]


class PrPcrypt(object):
    def __init__(self, key, iv=None):
        self.key = key[:16]
        self.iv = iv[:16]
        self.mode = AES.MODE_CBC

    def encrypt(self, text):
        text = pad(text)
        cryptor = AES.new(self.key.encode('utf-8'), self.mode, self.iv.encode('utf-8'))
        x = len(text) % 8
        if x != 0:
            text = text + '\0' * (8 - x)  # 不满16，32，64位补0
        self.ciphertext = cryptor.encrypt(text.encode('utf-8'))
        return base64.standard_b64encode(self.ciphertext).decode("utf-8")

    def decrypt(self, text):
        cryptor = AES.new(self.key.encode('utf-8'), self.mode, self.iv.encode('utf-8'))
        de_text = base64.standard_b64decode(text)
        plain_text = cryptor.decrypt(de_text)
        st = str(plain_text.decode("utf-8")).rstrip('\0')
        out = unpad(st)
        return out


pc = PrPcrypt('4c4d301d0fb4e483f84f8e73899b4e58', '1234577290ABCDEF1264147890ACAE45')  # 自己设定的密钥
e = pc.encrypt("ccqqq111")  # 加密内容
d = pc.decrypt(e)
print("加密后%s,解密后%s" % (e, d))
