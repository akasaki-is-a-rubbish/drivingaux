# -*- coding: UTF-8 -*
import getpass
import platform
from datetime import datetime
from termcolor import colored
from enum import Enum
import six


class Logger:
    def __init__(this, whom, ic=None, ic_color=None):
        this.ic = ""
        if ic is not None:
            ic = ic.value
            if ic_color is not None:
                ic = colored(ic, ic_color.value)
            this.ic = ic
        this.whom = whom

    def log(this, message, flag=None, with_ic=True):
        final_str = ''
        if flag is not None:
            final_str += flag
        if with_ic:
            final_str += this.ic
        final_str += str(this.whom) + ' > ' + str(datetime.now()) + " > " + message
        print(final_str)
        return this

    def err(this, err, flag=f"[{colored('×', 'red')}]"):
        this.log(err, flag)

    def banner(this, ch='=', length=80):
        print(ch * length)
        return this

    def print_os_info(this):
        print('whom\t\t|\t' + getpass.getuser() + " using " + str(platform.node()))
        print('machine\t\t|\t' + str(platform.machine()) + ' on ' + str(platform.processor()))
        print('system\t\t|\t' + str(platform.system()) + str(platform.version()))
        print('python\t\t|\t' + str(platform.python_build()) + ", ver " + platform.python_version())
        return this

    def gap(this, line_cnt=1):
        print('\n' * line_cnt)
        return this

    def print_txt_file(this, file):
        if isinstance(file, six.string_types):
            file = open(file)
        str = ''
        for line in file.readlines():
            str += line
        print(str)
        return this


class IconMode(Enum):
    setting = "⚙"
    star_filled = "★"
    star = "☆"
    circle = "○"
    circle_filled = "●"
    telephone_filled = "☎"
    telephone = "☏"
    smile = "☺"
    smile_filled = "☻"
    jap_no = "の"
    sakura_filled = "✿"
    sakura = "❀"
    java = "♨"
    music = "♪"
    block = "▧"
    left = "⇐"
    up = "⇑"
    right = "⇒"
    down = "⇓"
    left_right = "↹"


class IconColor(Enum):
    grey = "grey"
    red = "red"
    green = "green"
    yellow = "yellow"
    blue = "blue"
    magenta = "magenta"
    cyan = "cyan"
    white = "white"
