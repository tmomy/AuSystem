#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/8/29 10:11
"""
from .. import engine, ModelBase, err_logging
from app.conf import msg
from framework.utils import package_import
package_import("app.Tables")


@err_logging
def create_all_table():
    ModelBase.metadata.create_all(bind=engine)
    return True, msg.SUCCESS


@err_logging
def drop_all_table():
    ModelBase.metadata.drop_all(bind=engine)
    return True, msg.SUCCESS

