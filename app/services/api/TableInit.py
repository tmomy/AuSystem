#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/8/29 10:11
"""
from app.services import ModelBase,engine
from framework.utils import package_import
package_import("app.services.Tables")


def create_table():
    ModelBase.metadata.create_all(bind=engine)
    return True