import random


def generrator_account():
    """ 账号生成器 """

    character = []
    all_ = ['_']
    # 所有大写字母
    for i in range(65, 91):
        character.append(chr(i))
        all_.append(chr(i))
    # 所有小写字母
    for i in range(97, 123):
        character.append(chr(i))
        all_.append(chr(i))
    # 所有数字
    for i in range(48, 58):
        all_.append(chr(i))
    account_len = random.randint(3, 16)
    account = ''
    for i in range(account_len):
        if i == 0:
            account += random.choice(character)
        else:
            account += random.choice(all_)
    if len(account) < 3 or len(account) > 16:
        generrator_account()
    if account.endswith('_'):
        generrator_account()
    return account


def generrator_pass():
    num = []
    for i in range(48, 58):
        num.append(chr(i))
    pass_ = ''
    for i in range(random.randint(6, 10)):
        pass_ += random.choice(num)
    return str(pass_)