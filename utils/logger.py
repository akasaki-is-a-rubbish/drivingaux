# -*- coding: UTF-8 -*
import getpass
import platform
from datetime import datetime


class Logger:
    def __init__(self, whom):
        self.whom = whom

    def log(self, message, flag=None):
        final_str = ''
        if flag is not None:
            final_str += flag
        final_str += str(self.whom) + ' > ' + str(datetime.now()) + " > " + message
        print(final_str)
        return self

    def err(self, err, flag='[×]'):
        self.log(err, flag)

    def banner(self, ch='=', length=80):
        print(ch * length)
        return self

    def print_os_info(self):
        print('whom\t\t|\t' + getpass.getuser() + " using " + str(platform.node()))
        print('machine\t\t|\t' + str(platform.machine()) + ' on ' + str(platform.processor()))
        print('system\t\t|\t' + str(platform.system()) + str(platform.version()))
        print('python\t\t|\t' + str(platform.python_build()) + ", ver " + platform.python_version())
        return self

    def gap(self, line_cnt=1):
        print('\n' * line_cnt)
        return self
