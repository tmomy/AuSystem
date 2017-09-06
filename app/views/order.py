#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2017/8/30 10:52
"""
from app.untils import get_params
from app.framework_api import route, build_ret, get_ret
from app.services.api import OrderServices



# 订单操作
# 增加
@route("/order/add", api="order", methods=['GET', 'POST'])
def order():
    params = get_params()
    result = OrderServices.service_order_add(params)
    return build_ret(success=result)


# 查询
@route("/order/list", api="order", methods=['GET', 'POST'])
def list_order():
    params = get_params()
    result, total = OrderServices.service_order_list(params)
    return build_ret(success=True, data=result, total=total)


# 订单详情
@route("/order/detail", api="order", methods=['GET', 'POST'])
def detail_order():
    params = get_params()
    result = OrderServices.service_order_detail(params['order_num'])
    return build_ret(success=True, data=result, total=1)


# 修改订单状态
@route("/order/status/modify", api="order", methods=['GET', 'POST'])
def modify_order_status():
    params = get_params()
    result = OrderServices.service_order_modify_status(params)
    msg = ('操作成功！' if result else '操作失败！')
    return build_ret(success=result, msg=msg)


# 绑定订单运单号
@route("/order/express/modify", api="order", methods=['GET', 'POST'])
def modify_order_express():
    params = get_params()
    result = OrderServices.service_order_modify_express(params)
    msg = ('操作成功！' if result else '操作失败！')
    return build_ret(success=result, msg=msg)


# 任务模块
# 增加
@route("/task/add", api="task", methods=['GET', 'POST'])
def add_task():
    params = get_params()
    result = OrderServices.service_task_add(params)
    msg = ('操作成功！' if result else '操作失败，请检查余额！')
    return build_ret(success=result, msg=msg)


# 查询
@route("/task/list", api="task", methods=['GET', 'POST'])
def list_task():
    params = get_params()
    result, total = OrderServices.service_task_list(params)
    return build_ret(success=True, data=result, total=total)


# 删除
@route("/task/del", api="task", methods=['GET', 'POST'])
def del_task():
    # params = get_params()
    # result = task.task_del()
    result = OrderServices.service_task_del()
    return build_ret(success=result)

# 创建订单模块
# 自动生成订单
@route("/order/create", api="task", methods=['GET', 'POST'])
def create_order():
    # params = get_params()
    result = OrderServices.service_create_order()
    return build_ret(success=result)