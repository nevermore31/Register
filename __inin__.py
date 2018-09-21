import base64
from Crypto.Cipher import AES


# str不是16的倍数那就补足为16的倍数
def add_to_16(value):
    while len(value) % 16 != 0:
        value += '\0'
    return str.encode(value)  # 返回bytes

key = 'c0ca706c304fa317ded8ca26f1ad7521'  # 密码
text = 'dadssada123131'  # 待加密文本
aes = AES.new(add_to_16(key), AES.MODE_ECB)  # 初始化加密器
encrypted_text = str(base64.encodebytes(aes.encrypt(add_to_16(text))), encoding='utf-8').replace('\n', '')  # 执行加密并转码返回bytes
print(encrypted_text)
