import requests

TITLE = "NJU Health Checkin"


def pushplus_message(token, message, title=TITLE):
    payload = {'token': token, "channel": "wechat", "template": "html", "content": message, "title": TITLE}
    resp = requests.post("http://www.pushplus.plus/send", params=payload)
    if resp.status_code == 200:
        print('pushplus success code:', resp.status_code)
    else:
        print('push message to pushplus error,the code is:', resp.status_code)
    resp.close()
