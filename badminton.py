import json
import requests
import time
from urllib.parse import quote
from datetime import datetime

result_num = 0  


def order_it(begin_time, end_time, today_or_tomorrow, jwt_user_token, openid, headers):
    """
    根据指定的时间段、日期、jwt令牌和openid进行场地预约。
    """
    checkdata_s = f'[{{"FieldNo":"","FieldTypeNo":"YMQ01","BeginTime":"{begin_time}","Endtime":"{end_time}","Price":"0.00"}}]'
    checkdata = quote(checkdata_s)
    url = f'http://changguan.cuc.edu.cn/Field/OrderFieldGR?VenueNo=002&FieldTypeNo=YMQ01&dateadd={today_or_tomorrow}&checkdata={checkdata}'
    print(url)

    cookie = {
        'JWTUserToken': jwt_user_token,
        'OpenId': openid,
    }
    s = requests.Session()
    s.cookies.update(cookie)

    # 发送请求并处理响应
    response = s.get(url, headers=headers)
    resultjson = json.loads(response.text)
    if resultjson['message'] != '当前时间段未找到合适空闲场地，请刷新界面重新选择时间段！':
        global result_num
        result_num += 1
    print(response.text)


def main(begin_time, today_or_tomorrow, jwt_user_token, openid, headers):
    """
    根据指定的开始时间、日期、jwt令牌和openid预约场地。
    """
    end_time = f"{begin_time + 1}:00"
    begin_time = f"{begin_time}:00"
    order_it(begin_time, end_time, today_or_tomorrow,
             jwt_user_token, openid, headers)


if __name__ == "__main__":
    print("********************开始预约!************************")
    num = 1  # 这个参数表示你想约几个场，2代表四个场，2个场会自动停止程序

    # 请求头信息
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.47',
    }

    # 填写 Cookie
    users = []
    #id = 0
    user = {
        'jwt_user_token':'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiMjAyMjIwMTM1MTA1MjM5IiwiZXhwIjoxNzAyMDY2NTQwLjAsImp0aSI6ImxnIiwiaWF0IjoiMjAyMy0xMi0wNyAyMDoxNTo0MCJ9.1vSIFhYwqQaEq2YLT9KQpjAVCiNgtjOeifgoCmrGk8w',
        'OpenId':'202220135105239',
    }
    users.append(user)
    # id = 1
    user = {
        'jwt_user_token':'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiMjAyMjIwMTM1MTA1MjIxIiwiZXhwIjoxNzAyNTAyNTMyLjAsImp0aSI6ImxnIiwiaWF0IjoiMjAyMy0xMi0xMiAyMToyMjoxMiJ9.Z0Ja0yeO_c0nNSPpYHkvMOmNekpA4rUIlOoVsSfPAUA',
        'OpenId':'202220135105221',
    }
    users.append(user)
    # id = 2
    user = {
        'jwt_user_token':'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiMjAyMjIwMTM1MTA1MjM1IiwiZXhwIjoxNzAyMzIwODUxLjAsImp0aSI6ImxnIiwiaWF0IjoiMjAyMy0xMi0xMCAxODo1NDoxMCJ9.ogEYE0yQlwIZBs6Rl0Foxz7tDlTVPQXEjkr-aisRGvE',
        'OpenId':'202220135105235',
    }
    users.append(user)
    weekday = datetime.now().weekday() % 3
    id = 1
    jwt_user_token = users[id]['jwt_user_token']
    OpenId = users[id]['OpenId']



    # 构建Cookie
    headers["Cookie"] = f'JWTUserToken={jwt_user_token}; OpenId={OpenId}'

    while True:
        time_now = time.strftime("%H:%M:%S", time.localtime())
        # if "08:10:00" > time_now >= "07:50:00":  # 此处设置每天定时的时间，18表示下午六点-7点场，1表示预约明天的场，0表示今天的场
        main(19, 1, jwt_user_token, OpenId, headers)
        main(20, 1, jwt_user_token, OpenId, headers)

        # 检查是否达到预定的预约数量
        if result_num == num:
            print("预约成功!")
            break

        # 检查是否超过预定的预约时间
        if time_now >= "08:10:00":
            # print("预约超时!")
            # break
            pass