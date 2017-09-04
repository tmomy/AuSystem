#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2017/9/1 10:24
"""
import time, random
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.Tables.orderModel import Order
from app.Tables.taskModel import Task
from app.services.OrderManageService.order import order_add
from .. import engine, handler_commit

session = Session(engine)

def create_order():
    """
    :info
    @遍历所有用户（排除余额为0的）
    @根据每个用户和当天时间查询task记录
    @如果查到根据该条task记录则根据task记录扣除用户余额，生成订单
    @如果没查到则生成task_num为1的订单并且扣除余额
    :return: True or False
    """
    local_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    user_result = session.query(Order).filter(
        and_(
            Order.rest_day > 0
        ))
    for user in user_result:
        print user.user_id
        task_result = session.query(Task).filter(
            and_(
                Task.user_id == user.user_id,
                Task.task_do_time == local_date
            ))
        if task_result.count() is not 0:
            user.rest_day = user.rest_day - task_result.one().task_num
            # 生成订单--传参
            order_add()
        else:
            user.rest_day = user.rest_day - 1
            # 生成订单--传参
            order_add()

# if __name__ == '__main__':
#     create_order()
