import json


class Config(object):
    __conf_path = '../config/config.json'

    def __init__(self):
        with open(Config.__conf_path, encoding='utf-8') as cf:
            conf_dict = json.load(cf)

        for key, value in conf_dict.items():
            if isinstance(value, str) or isinstance(value, dict) or \
                    isinstance(value, int) or isinstance(value, float) or isinstance(value, list):
                setattr(self, key, value)