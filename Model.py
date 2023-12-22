import json
from datetime import datetime, timedelta

CONFIG_PATH = 'config.json'  # 配置文件路径



def load_config():
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)
    return config


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Model(metaclass=SingletonMeta):
    def __init__(self, config = None):
        if config is None:
            config = {}
        self.config = config

    def save_to_json(self, file_name):
        with open(file_name, 'w') as json_file:
            json.dump(self.config, json_file)

    def load_from_json(self, file_name):
        with open(file_name, 'r') as json_file:
            self.config = json.load(json_file)

    def initParams(self):
        config = load_config()

        self.name = config["USERS_INFO"][0]["name"]
        self.token = ""
        self.openid = config["USERS_INFO"][0]["OpenId"]
        self.begin_time1 = config["BOOKING"]["RESERVE_TIME_SLOT"][0]
        self.begin_time2 = config["BOOKING"]["RESERVE_TIME_SLOT"][1]

        self.bDebug = False
        self.bPause = False
        self.time1_ordered = False
        self.time2_ordered = False
        self.time1_needed = True
        self.time2_needed = True
        self.add_Day = 1
        self.started = False
        self.sum = 2

        weekday_options = ['周一', '周二', '周三', '周四', '周五', '周六', '周天']
        order_date = (datetime.now() + timedelta(days=2)).date()  # 后天日期
        order_weekday = order_date.weekday()
        self.order_weekday_str = weekday_options[ order_weekday ]