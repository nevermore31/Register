import time

a = 'wd_in_hy=5ba5bacf1fc166.19814741; ' \
    'FO_USER=dadaada223232; ' \
    '51uids=453996290%2C453808427%7C264b8918b6b43f110ac4eb4417afd4cb; ' \
    'FO_USER=qq333123131; ' \
    'FO_RFLP=%7CaHR0cDovL21pY3JvLjUxLmNvbS9jbGllbnQvaW5kZXgvaHkvP2Zyb209d2RoeSZzaXRlX2Nzcz0%3D%7C%7C%7C; ' \
    'FO_TUID=qRrxZm; ' \
    'PHPSESSID=a6r0noh0mk2ocmvgs3lcdjfb95; ' \
    '5bbe05e29b8e5=1539180261_4ed45a9cd181d1193404c7c27a758808; ' \
    'FO_JSONP_TOKEN=aa07e55abd90a8b7ec7213247215069c; ' \
    'FO_JSONP_TIME=1539180262'

b = 'FO_USER=dadaada223232; ' \
    '51uids=453996290%2C453808427%7C264b8918b6b43f110ac4eb4417afd4cb; ' \
    'FO_RFLP=%7CaHR0cDovL21pY3JvLjUxLmNvbS9jbGllbnQvaW5kZXgvaHkvP2Zyb209d2RoeSZzaXRlX2Nzcz0%3D%7C%7C%7C; ' \
    'FO_TUID=qRrxZm; ' \
    'PHPSESSID=qcs2hlbhq5ajp7qgae6ldu9h40; ' \
    '5bbe05e29b8e5=1539180261_4ed45a9cd181d1193404c7c27a758808; _' \
    'nei_from=port_wdhy; ' \
    '5bbe13f2b2de3=1539184338_192d37d493a7fa8815a1f5921f96dab0; ' \
    'FO_JSONP_TOKEN=114dc5c9f0cc47c411b74de80a1bf03f; ' \
    'FO_JSONP_TIME=1539184689'

c = 'FO_USER=dadaada223232; 51uids=453996290%2C453808427%7C264b8918b6b43f110ac4eb4417afd4cb; FO_RFLP=%7CaHR0cDovL21pY3JvLjUxLmNvbS9jbGllbnQvaW5kZXgvaHkvP2Zyb209d2RoeSZzaXRlX2Nzcz0%3D%7C%7C%7C; FO_TUID=qRrxZm; PHPSESSID=qcs2hlbhq5ajp7qgae6ldu9h40; 5bbe05e29b8e5=1539180261_4ed45a9cd181d1193404c7c27a758808; _nei_from=port_wdhy; 5bbe13f2b2de3=1539184338_192d37d493a7fa8815a1f5921f96dab0; FO_JSONP_TOKEN=41f047353f97204d0a4d1a65fa611c03; FO_JSONP_TIME=1539184340'

# a FO_USER 第二个与bc不同
a_ = ['wd_in_hy,(b没有)', '5bbe05e29b8e5', 'FO_USER', 'FO_JSONP_TOKEN', 'PHPSESSID']
bc_ = ['_nei_from(a没有)', '5bbe13f2b2de3', 'PHPSESSID','FO_JSONP_TOKEN']

