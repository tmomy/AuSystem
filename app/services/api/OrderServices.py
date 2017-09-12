#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2017/9/4 8:55
"""
from ..OrderManageService import OrderOperate, TaskOperate, CreateOrderOperate

# 订单接口

# service_order_add = OrderOperate.order_add
service_order_list = OrderOperate.order_list
service_order_detail = OrderOperate.order_detail
service_order_modify_status = OrderOperate.order_modify_status
service_order_modify_express = OrderOperate.order_modify_express
service_order_switch = OrderOperate.order_switch

# 任务接口

service_task_add = TaskOperate.task_add
service_task_list = TaskOperate.task_list
service_task_del = TaskOperate.task_del

# 生成订单接口

service_create_order = CreateOrderOperate.order_create
