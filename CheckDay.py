from Model import Model
from LogSys import print_with_time
from datetime import datetime, timedelta
import time
import requests
import json



order_begin_logged = False
order_waiting_logged = False


def check_day():
    model = Model()

    headers = model.config['HEADERS'].copy()

    url = f"https://changguan.cuc.edu.cn/Field/GetWeek?VenueNo=002"

    Cookie = {
        'JWTUserToken': model.token,
        'OpenId': model.openid
    }

    s = requests.Session()
    s.cookies.update(Cookie)

    # response
    response = s.get(url, headers=headers)

    try:
        result_json = json.loads(response.text)
    except json.decoder.JSONDecodeError as e:
        print_with_time(f"小助手温馨提示：{model.name} 的Token可能过期了！。")
        # model.bPause = True
        return 0

    backend_weekday_str = result_json[1]["Week"]

    global order_begin_logged
    global order_waiting_logged

    # 第二天的抢票已经开放
    if model.order_weekday_str == backend_weekday_str :
        if order_begin_logged == False :
            print_with_time(f"第二天{model.order_weekday_str}的抢票开放了！！！全速出击！！！")
            order_begin_logged = True
        return 1
    else :
        if order_waiting_logged == False :
            print_with_time(f"{model.order_weekday_str}的抢票还没开始。小助手会在系统开放的第一时间出击！")
            order_waiting_logged = True
        return 0










