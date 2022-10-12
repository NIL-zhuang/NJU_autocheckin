# %%
import datetime
import os
import random
from hashlib import md5
from time import sleep

import requests

from message import pushplus_message

SLEEP_TIME = 60  # 睡眠的时间范围，单位：秒

# 打卡前进行一次随机时长的睡眠
print(f"Triggered at {datetime.datetime.now()}")
rand_time = random.random() * SLEEP_TIME
print(f"Scheduled at {datetime.datetime.now() + datetime.timedelta(seconds=rand_time)}")
sleep(rand_time)
print(f"Started at {datetime.datetime.now()}")

CASTGC = os.environ['CASTGC']   # https://authserver.nju.edu.cn/ storage/COOKIES的CASTGC
PUSHPLUS_TOKEN = os.environ['PUSHPLUS_TOKEN']   # 你所设置的pushplus的token

session = requests.Session()
response = session.get(
    url=r'http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/getApplyInfoList.do',
    headers={
        'User-Agent': 'cpdaily/9.0.15 wisedu/9.0.15',
        'Referer': 'http://ehallapp.nju.edu.cn/xgfw/sys/mrjkdkappnju/index.html'
    },
    cookies={'CASTGC': CASTGC}
)

# 获取上一次打卡的信息
try:
    content = response.json()
except ValueError:
    content = {}
print(f"List: {response.status_code}, {response.reason}, {content.get('msg') or 'No messgage available'}")
if not (response.status_code == 200 and content.get('code') == '0'):
    if PUSHPLUS_TOKEN:
        pushplus_message(PUSHPLUS_TOKEN, f"获取上一次打卡信息失败，状态码：{response.status_code}，原因：{response.reason}")
    exit(0)

data = next(x for x in content['data'] if x.get('TJSJ') != '')
wid = content['data'][0]['WID']

# get MD5
response = session.get(
    url=r'http://ehallapp.nju.edu.cn/xgfw//sys/yqfxmrjkdkappnju/apply/getMd5Value.do',
    headers={
        'User-Agent': 'cpdaily/9.0.15 wisedu/9.0.15',
        'Referer': 'http://ehallapp.nju.edu.cn/xgfw/sys/mrjkdkappnju/index.html'
    },
    cookies={'CASTGC': CASTGC}
)

try:
    content = response.text
except ValueError:
    content = {}
print(f"MD5: {response.status_code}, {response.reason or 'No messgage available}'}")
md5_value = content


# %% apply
data_apply = {
    'CURR_LOCATION': data['CURR_LOCATION'],
    'IS_HAS_JKQK': data['IS_HAS_JKQK'],
    'IS_TWZC': data['IS_TWZC'],
    'JRSKMYS': data['JRSKMYS'],
    'JZRJRSKMYS': data['JZRJRSKMYS'],
    'SFZJLN': data['SFZJLN'],
    'WID': wid,
    'ZJHSJCSJ': (datetime.datetime.now() - random.randint(0, 1) * datetime.timedelta(days=1)).strftime(r'%Y-%m-%d') + ' %02d' % (random.randint(8, 16))
}
data_apply['sign'] = md5('|'.join(list(data_apply.values()) + [md5_value]).encode("utf-8")).hexdigest()

print(data_apply)

response = session.get(
    url=r'http://ehallapp.nju.edu.cn/xgfw//sys/yqfxmrjkdkappnju/apply/saveApplyInfos.do',
    params=data_apply,
    headers={
        'User-Agent': 'cpdaily/9.0.15 wisedu/9.0.15',
        'Referer': 'http://ehallapp.nju.edu.cn/xgfw/sys/mrjkdkappnju/index.html'
    },
    cookies={'CASTGC': CASTGC}
)

try:
    content = response.json()
except ValueError:
    content = {}

msg = f"Apply: {response.status_code}, {response.reason}, {content.get('msg') or 'No messgage available'}, {data_apply}"
if response.status_code == 200 and content.get('code') == '0':
    print('Finished at %s' % (datetime.datetime.now()))
    print(msg)
    if PUSHPLUS_TOKEN:
        pushplus_message(PUSHPLUS_TOKEN, msg)
