import json

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
        self.bDebug = False
        self.time1_ordered = False
        self.time2_ordered = False
        self.time1_needed = True
        self.time2_needed = True