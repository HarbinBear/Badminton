import codecs
import json
import time
from datetime import datetime, timedelta
from urllib.parse import quote
from LogSys import print_with_time
from Model import Model
import calendar


import requests

CONFIG_PATH = 'config.json'  # 配置文件路径
bLogUrl = False
bPause = False

def load_config():
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)
    return config


def order_it(  begin_time, end_time, today_or_tomorrow ):
    model = Model()

    headers = model.config['HEADERS'].copy()

    checkdata_s = f'[{{' \
                  f'"FieldNo":"",' \
                  f'"FieldTypeNo":"YMQ01",' \
                  f'"BeginTime":"{begin_time}",' \
                  f'"Endtime":"{end_time}",' \
                  f'"Price":"0.00"' \
                  f'}}]'

    checkdata = quote(checkdata_s)
    url = f'http://changguan.cuc.edu.cn/Field/OrderFieldGR?VenueNo=002&FieldTypeNo=YMQ01&dateadd={today_or_tomorrow}&checkdata={checkdata}'
    global  bLogUrl
    if bLogUrl == False :
        print_with_time(url)
        bLogUrl = True

    # params = {
    #     'VenueNo':'002',
    #     'FieldTypeNo':'YMQ01',
    #     'dateadd':today_or_tomorrow,
    #     'checkdata':checkdata
    # }
    # 构建Cookie
    Cookie = {
        'JWTUserToken' : model.token,
        'OpenId' : model.openid
    }

    s = requests.Session()
    s.cookies.update(Cookie)

    # response
    response = s.get(url, headers=headers  )

    try:
        result_json = json.loads( response.text )
    except json.decoder.JSONDecodeError as e:
        print_with_time("小助手温馨提示：您的Token可能过期了！。")
        global bPause
        bPause = True


    order_date = (datetime.now() + timedelta(days=1)).date()  # 明天日期
    week_days = ['周一', '周二', '周三', '周四', '周五', '周六', '周天']
    weekday = order_date.weekday()

    if result_json['type'] == 1 :
        print_with_time(f"成功预约 {order_date} {week_days[weekday]} 的 {begin_time} 到 {end_time} 的场子！！！")
        # 这个时段的都不用抢了
        if begin_time == model.begin_time1 :
            model.time1_ordered = True
        if begin_time == model.begin_time2 :
            model.time2_ordered = True
        return 1
    else:
        print_with_time(f"没约到 {order_date} {week_days[weekday]} 的 {begin_time} 到 {end_time} 的场子，"
                        f"因为：{result_json['message']}")
        return 0


def book( ):
    model = Model()

    print_with_time("********************开始预约!************************")
    result_num = 0

    print_with_time("OpenID: {openid}".format( openid = model.openid ) )
    print_with_time("JWTUserToken: {token}".format( token = model.token ) )
    if model.time1_needed == True:
        print_with_time("第一个场: {start1}:00 ~ {end1}:00 ".format( start1 = model.begin_time1 , end1 = model.begin_time1+1 ) )
    if model.time2_needed == True:
        print_with_time("第二个场: {start2}:00 ~ {end2}:00 ".format( start2 = model.begin_time2 , end2 = model.begin_time2+1 ) )

    while result_num < model.config['BOOKING']['NUM_OF_VENUES']:

        if bPause == True:
            break

        time_now = datetime.now().time()
        time_now_str = time_now.strftime("%H:%M:%S")

        if model.debug_var.get() == True or model.config['BOOKING']['END_BOOKING_AT'] > time_now_str >= model.config['BOOKING']['START_BOOKING_AT']: #  开约条件

            if model.time1_needed == True and model.time1_ordered == False :
                result = order_it(f"{model.begin_time1}:00", f"{model.begin_time1 + 1}:00", 0)
                result_num += result

            if model.time2_needed == True and model.time2_ordered == False :
                result = order_it(f"{model.begin_time2}:00", f"{model.begin_time2 + 1}:00", 0)
                result_num += result

        # 检查是否达到预定的预约数量
        if result_num == model.config['BOOKING']['NUM_OF_VENUES']:
            print_with_time(f"小助手今日任务完成!总共约到了{result_num}个场子！")
            break
        # time.sleep(2)


