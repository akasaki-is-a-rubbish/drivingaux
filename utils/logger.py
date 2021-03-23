# -*- coding: UTF-8 -*
import getpass
import platform
from datetime import datetime


class Logger:
    def __init__(this, whom):
        this.whom = whom

    def log(this, message, flag=None):
        final_str = ''
        if flag is not None:
            final_str += flag
        final_str += str(this.whom) + ' > ' + str(datetime.now()) + " > " + message
        print(final_str)
        return this

    def err(this, err, flag='[×]'):
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
