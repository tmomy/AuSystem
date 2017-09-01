#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2017/8/30 10:52
"""
from app.untils import get_params
from app.framework_api import route, build_ret, get_ret
from app.services.OrderManageService.order import order_add, order_list, order_modify
from app.services.OrderManageService.task import task_add, task_list, task_del
from app.services.api.TableInit import create_all_table


# 订单操作
# 增加
@route("/add/order", api="order", methods=['GET', 'POST'])
def order():
    # params = get_params()
    create_all_table()
    result = order_add()
    return build_ret(success=result)


# 查询
@route("/list/order", api="order", methods=['GET', 'POST'])
def list_order():
    # params = get_params()
    result, total = order_list()
    return build_ret(success=True, data=result, total=total)


# 编辑
@route("/modify/order", api="order", methods=['GET', 'POST'])
def modify_order():
    # params = get_params()
    result = order_modify()
    return build_ret(success=result)


# 任务模块
# 增加
@route("/add/task", api="task", methods=['GET', 'POST'])
def add_task():
    # params = get_params()
    create_all_table()
    result = task_add()
    return build_ret(success=result)


# 查询
@route("/list/task", api="task", methods=['GET', 'POST'])
def list_task():
    # params = get_params()
    result, total = task_list()
    return build_ret(success=True, data=result, total=total)


# 删除
@route("/del/task", api="task", methods=['GET', 'POST'])
def del_task():
    # params = get_params()
    result = task_del()
    return build_ret(success=result)
