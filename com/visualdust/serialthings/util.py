import json
from com.visualdust.serialthings.dist4x import Dist4x
from com.visualdust.serialthings.lidar import Lidar

def parse_dict(config, name=None):
    if config["type"] == Dist4x.__name__:
        return Dist4x(config["port"], config["baudrate"], name)
    if config["type"] == Lidar.__name__:
        return Lidar(config["port"], name)


def parse_all(config_for_all):
    result = []
    for item in config_for_all:
        result.append(parse_dict(config_for_all[item], name=item))
    return result


def parse_file(config_file):
    if type(config_file) == str:
        config_file = open(config_file)
    configs = json.load(config_file)
    return parse_all(configs)