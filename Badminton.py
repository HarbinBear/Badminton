import codecs
import json
import time
from datetime import datetime, timedelta
from urllib.parse import quote
from LogSys import print_with_time


import requests

CONFIG_PATH = 'config.json'  # 配置文件路径
bLogUrl = False
bPause = False

def load_config():
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)
    return config


def order_it( config , openid , token , begin_time, end_time, today_or_tomorrow):


    headers = config['HEADERS'].copy()

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
        'JWTUserToken' : token,
        'OpenId' : openid
    }



    s = requests.Session()
    s.cookies.update(Cookie)


    # response
    response = s.get(url, headers=headers  )


    try:
        result_json = json.loads( response.text )
    except json.decoder.JSONDecodeError as e:
        print_with_time("Token过期了吧。")
        global bPause
        bPause = True


    print_with_time(result_json['message'])

    if result_json['type'] == 1 :
        print_with_time("成功预约")
        return 1
    else:
        return 0




def book( openid , token , begin_time1 , begin_time2 ):
    config = load_config()

    print_with_time("********************开始预约!************************")
    result_num = 0

    print_with_time("OpenID: {openid}".format( openid = openid ) )
    print_with_time("JWTUserToken: {token}".format( token = token ) )
    print_with_time("第一个场: {start1}:00 ~ {end1}:00 ".format( start1 = begin_time1 , end1 = begin_time1+1 ) )
    print_with_time("第二个场: {start2}:00 ~ {end2}:00 ".format( start2 = begin_time2 , end2 = begin_time2+1 ) )

    while result_num < config['BOOKING']['NUM_OF_VENUES']:

        if bPause == True:
            break

        time_now = datetime.now().time()
        time_now_str = time_now.strftime("%H:%M:%S")

        if config['BOOKING']['END_BOOKING_AT'] > time_now_str >= config['BOOKING']['START_BOOKING_AT']:
        # if 1 :
            # order_date = (datetime.now() + timedelta(days=1)).date()
            # index = datetime.now().weekday() % len(config['USERS_INFO'])
            for begin_time in config['BOOKING']['RESERVE_TIME_SLOT']:
                result = order_it( config , openid , token , f"{begin_time}:00", f"{begin_time + 1}:00", 0)
                result_num += result

        # 检查是否达到预定的预约数量
        if result_num == config['BOOKING']['NUM_OF_VENUES']:
            print_with_time("预约成功!")

        time.sleep(5)


