import codecs
import json
from datetime import datetime, timedelta
from urllib.parse import quote

import requests

CONFIG_PATH = 'config.json'  # 配置文件路径


def load_config():
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)
    return config


def order_it(config, user_index, begin_time, end_time, today_or_tomorrow):
    user_info = config['USERS_INFO'][user_index]
    headers = config['HEADERS'].copy()

    checkdata_s = f'[{{"FieldNo":"","FieldTypeNo":"YMQ01","BeginTime":"{begin_time}","Endtime":"{end_time}","Price":"0.00"}}]'
    checkdata = quote(checkdata_s)
    # url = f'http://changguan.cuc.edu.cn/Field/OrderFieldGR?VenueNo=002&FieldTypeNo=YMQ01&dateadd={today_or_tomorrow}&checkdata={checkdata}'
    url = f'http://changguan.cuc.edu.cn/Field/OrderFieldGR'

    params = {
        'VenueNo':'002',
        # 'VenueNo':'001',
        'FieldTypeNo':'YMQ01',
        # 'FieldTypeNo':'LQ01',
        'dateadd':today_or_tomorrow,
        'checkdata':checkdata
    }
    # 构建Cookie
    headers["Cookie"] = \
        f'JWTUserToken={user_info["JWTUserToken"]}; ' \
        f'OpenId={user_info["OpenId"]} ;'

    # response
    response = requests.get(url, headers=headers , params=params )


    # dec1
    result_json = response.json()

    # dec2
    # content = response.text.encode().decode('utf-8-sig')
    # result_json = json.loads( content )

    # dec3
    # decode_data = codecs.decode( response.text.encode() , 'utf-8-sig' )
    # result_json = json.loads(decode_data)

    if result_json.get('message') != '当前时间段未找到合适空闲场地，请刷新界面重新选择时间段！':
        return 1
    else:
        return 0




def main():
    config = load_config()

    print("********************开始预约!************************")
    result_num = 0
    while result_num < config['BOOKING']['NUM_OF_VENUES']:

        time_now = datetime.now().time()
        time_now_str = time_now.strftime("%H:%M:%S")

        # if config['BOOKING']['END_BOOKING_AT'] > time_now_str >= config['BOOKING']['START_BOOKING_AT']:
        if 1 :
            order_date = (datetime.now() + timedelta(days=1)).date()
            index = datetime.now().weekday() % len(config['USERS_INFO'])
            for begin_time in config['BOOKING']['RESERVE_TIME_SLOT']:
                result = order_it(config, index, f"{begin_time}:00", f"{begin_time + 1}:00", order_date)
                result_num += result

        # 检查是否达到预定的预约数量
        if result_num == config['BOOKING']['NUM_OF_VENUES']:
            print("预约成功!")


if __name__ == "__main__":
    main()


