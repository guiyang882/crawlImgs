# -*- coding: utf-8 -*-
# @Time    : 2017/5/9 16:48
# @Author  : liuguiyangnwpu@gmail.com
# @File    : test.py
# @Software: PyCharm

from __future__ import absolute_import
from __future__ import print_function

import _datetime
import time

a = _datetime.datetime.now()
delta = _datetime.timedelta(minutes=30)
b = a - delta
print(int(time.mktime(b.timetuple())))