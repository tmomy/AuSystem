#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/8/25 17:33
"""
from app.conf.config import log,web
from app.conf import msg
from app.untils.log_builder import build_log
from sqlalchemy.ext.declarative import declarative_base
from functools import wraps
from app.mysql_db import db_pool
import traceback
import threading

_idnt = threading._get_ident()

ModelBase = declarative_base()
engine = db_pool
sys_logging = build_log(log)


def handler_commit(fun):
    try:
        fun.commit()
        return True, msg.SUCCESS
    except:
        fun.rollback()
        sys_logging.debug("mysql.query.one.err_id:{}{}".format(_idnt, traceback.format_exc()))
        return False, msg.ERROR(_idnt, "操作失败！")


def err_logging(func):
    @wraps(func)
    def deco(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except:
            sys_logging.debug("mysql.query.one.err_id:{}{}".format(_idnt,traceback.format_exc()))
            return False, msg.ERROR(_idnt, "操作失败！")

    return deco


# 更新字段值
def field_update(table, field, value=1):
    if not hasattr(table, field):
        return False
    setattr(table,field,value)
    return table

