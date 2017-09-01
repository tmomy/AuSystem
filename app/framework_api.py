#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/8/26 17:05
"""
from framework.decorators import route
from framework.utils import build_ret
from framework.utils.common import get_ret
from framework.utils.common import date_time
from framework.db import db

redis_service = db['redis']

