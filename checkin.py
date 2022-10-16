# %%
import datetime
import os
import random
from hashlib import md5
from time import sleep

import requests

from message import pushplus_message

SLEEP_TIME = 300  # 睡眠的时间范围，单位：秒
USER_AGENT = "Dalvik/2.1.0 (Linux; U; Android 12; 22011211C Build/SP1A.210812.016)"  # 安卓客户端的user-agent
REFER = r"http://ehallapp.nju.edu.cn/xgfw/sys/mrjkdkappnju/index.html"
GET_APPLY_INFO_URL = r"http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/getApplyInfoList.do"
GET_MD5_VALUE_URL = r"http://ehallapp.nju.edu.cn/xgfw//sys/yqfxmrjkdkappnju/apply/getMd5Value.do"
SAVE_APPLY_INFO_URL = r"http://ehallapp.nju.edu.cn/xgfw//sys/yqfxmrjkdkappnju/apply/saveApplyInfos.do"

PUSHPLUS_SUCCESS = "Success NJU Health Checkin"
PUSHPLUS_FAIL = "Fail NJU Health Checkin"

HEADERS = {
    'User-Agent': USER_AGENT,
    'Referer': REFER,
}
CASTGC = os.environ.get('CASTGC', None)   # https://authserver.nju.edu.cn/ storage/COOKIES的CASTGC
PUSHPLUS_TOKEN = os.environ.get('PUSHPLUS_TOKEN', None)   # 你所设置的pushplus的token，可以为空
COOKIE = {'CASTGC': CASTGC}

# 打卡前进行一次随机时长的睡眠
print(f"Triggered at {datetime.datetime.now()}")
rand_time = random.random() * SLEEP_TIME
print(f"Scheduled at {datetime.datetime.now() + datetime.timedelta(seconds=rand_time)}")
sleep(rand_time)
print(f"Started at {datetime.datetime.now()}")


# 获取上一次打卡的信息
session = requests.Session()
response = session.get(
    url=GET_APPLY_INFO_URL,
    headers=HEADERS,
    cookies={'CASTGC': CASTGC}
)
try:
    content = response.json()
except ValueError:
    content = {}
print(f"List: {response.status_code}, {response.reason}, {content.get('msg') or 'No messgage available'}")
if not (response.status_code == 200 and content.get('code') == '0'):
    if PUSHPLUS_TOKEN:
        pushplus_message(PUSHPLUS_TOKEN, f"获取上一次打卡信息失败，状态码：{response.status_code}，原因：{response.reason}", title=PUSHPLUS_SUCCESS)
    exit(0)

data = next(x for x in content['data'] if x.get('TJSJ') != '')
wid = content['data'][0]['WID']

# get MD5
response = session.get(
    url=GET_MD5_VALUE_URL,
    headers=HEADERS,
    cookies=COOKIE
)
try:
    content = response.text
except ValueError:
    content = {}
print(f"MD5: {response.status_code}, {response.reason or 'No messgage available}'}")
md5_value = content

# Apply for checkin
hesuan_time = (datetime.datetime.now() - random.randint(0, 1) * datetime.timedelta(days=1)).strftime(r'%Y-%m-%d') + ' %02d' % (random.randint(8, 16))
data_apply = {
    'CURR_LOCATION': data['CURR_LOCATION'],
    'IS_HAS_JKQK': data['IS_HAS_JKQK'],
    'IS_TWZC': data['IS_TWZC'],
    'JRSKMYS': data['JRSKMYS'],
    'JZRJRSKMYS': data['JZRJRSKMYS'],
    'SFZJLN': data['SFZJLN'],
    'WID': wid,
    'ZJHSJCSJ': hesuan_time,
}
data_apply['sign'] = md5('|'.join(list(data_apply.values()) + [md5_value]).encode("utf-8")).hexdigest()
print(data_apply)

response = session.get(
    url=SAVE_APPLY_INFO_URL,
    params=data_apply,
    headers=HEADERS,
    cookies=COOKIE,
)
try:
    content = response.json()
except ValueError:
    content = {}

# 反馈结果
msg = f"Apply: {response.status_code}, {response.reason}, {content.get('msg') or 'No messgage available'}, {data_apply}"
if response.status_code == 200 and content.get('code') == '0':
    print('Finished at %s' % (datetime.datetime.now()))
    print(msg)
    if PUSHPLUS_TOKEN:
        pushplus_message(PUSHPLUS_TOKEN, msg, title=PUSHPLUS_SUCCESS)
else:
    if PUSHPLUS_TOKEN:
        pushplus_message(PUSHPLUS_TOKEN, msg, title=PUSHPLUS_FAIL)
