#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/8/25 17:33
"""
from app.conf.config import log
from app.untils.log_builder import build_log
from sqlalchemy.ext.declarative import declarative_base
from app.mysql_db import db_pool
import traceback


ModelBase = declarative_base()
engine = db_pool
sys_logging = build_log(log)


def handler_commit(fun):
        try:
            result = fun()
            return result
        except Exception as e:
            sys_logging.debug("create pool err:{}".format(traceback.print_exc()))
            return False

