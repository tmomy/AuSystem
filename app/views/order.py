#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2017/8/30 10:52
"""
from app.untils import get_params
from app.framework_api import route, build_ret, get_ret
from app.services.OrderManageService.order import order_add, order_list, order_modify
from app.services.api.TableInit import create_all_table


@route("/add/order", api="测试", methods=['GET', 'POST'])
def order():
    # params = get_params()
    create_all_table()
    result = order_add()
    return build_ret(success=True)

@route("/list/order", api="测试", methods=['GET', 'POST'])
def list_order():
    # params = get_params()
    result, total = order_list()
    return build_ret(success=True, data=result, total=total)


@route("/modify/order", api="测试", methods=['GET', 'POST'])
def modify_order():
    # params = get_params()
    result = order_modify()
    return build_ret(success=result)