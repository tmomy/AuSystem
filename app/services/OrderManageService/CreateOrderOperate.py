#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2017/9/1 10:24
"""
import time, random
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.Tables.OrderModel import Order, BalanceRecord
from app.Tables.TaskModel import Task
from app.Tables.userModel import User
from app.Tables.PackageModel import Package
from app.Tables.AccountAddress import Address
from .. import engine, handler_commit

session = Session(engine)


# 废弃
def order_create_old():
    """
    :info
    @遍历所有用户（排除余额为0的）
    @根据每个用户和当天时间查询task记录
    @如果查到根据该条task记录则根据task记录扣除用户余额，生成订单
    @如果没查到则生成task_num为1的订单并且扣除余额
    :return: True or False
    """
    local_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    package_result = session.query(Package).filter(
        and_(
            Package.effect_time.like('%' + local_date + '%')
        ))
    if package_result.count() is 1:
        # 获取当日package_id
        package_id = package_result.one().package_id
    else:
        # 如果当日没有package则生成订单失败
        return '当日package不存在'

    user_result = session.query(User).filter(
        and_(
            User.rest_day > 0
        ))
    for user in user_result:
        task_result = session.query(Task).filter(
            and_(
                Task.user_id == user.user_id,
                Task.task_do_time == local_date
            ))
        order_result = session.query(Order).filter(
            and_(
                Order.user_id == user.user_id,
                Order.order_time.like('%' + local_date + '%')
            ))
        address_result = session.query(Address).filter(
            and_(
                Address.user_id == user.user_id,
                Address.default == 0
            ))
        # 判断用户是否存在默认地址
        if address_result.count() is 1:
            # 判断当天订单是否存在
            if order_result.count() is 0:
                if task_result.count() is not 0:
                    user.rest_day = user.rest_day - task_result.one().task_num
                    # 生成订单--传参
                    if task_result.one().task_num is not 0:
                        session.add(Order(order_num=__order_num(user_id=user.user_id, package_id=package_id,), user_id=user.user_id, package_id=package_id,
                                      order_status=0, order_package_num=task_result.one().task_num, address_id=address_result.one().id))
                else:
                    user.rest_day = user.rest_day - 1
                    # 生成订单--传参
                    session.add(Order(order_num=__order_num(user_id=user.user_id, package_id=package_id,), user_id=user.user_id, package_id=package_id,
                                  order_status=0, order_package_num=1, address_id=address_result.one().id))
    result = handler_commit(session)
    return result


def order_create():
    """
    :info
    @遍历所有用户（排除余额为0的和开关为0的生效时间<=当前时间）
    @符合条件的用户生成当日订单
    :return: True or False
    """
    local_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    package_result = session.query(Package).filter(
        and_(
            Package.effect_time.like('%' + local_date + '%')
        ))
    if package_result.count() is 1:
        # 获取当日package_id
        package_id = package_result.one().package_id
    else:
        # 如果当日没有package则生成订单失败
        return '当日package不存在'

    user_result = session.query(User).filter(
        and_(
            User.rest_day > 0,
            User.switch == 1,
            User.effective_time.between('1017-09-08', local_date)
        ))
    for user in user_result:
        order_result = session.query(Order).filter(
            and_(
                Order.user_id == user.user_id,
                Order.order_time.like('%' + local_date + '%')
            ))
        address_result = session.query(Address).filter(
            and_(
                Address.user_id == user.user_id,
                Address.default == 0
            ))
        # 判断用户是否存在默认地址
        if address_result.count() is 1:
            # 判断当天订单是否存在
            if order_result.count() is 0:
                user.rest_day = user.rest_day - 1
                # 生成订单--传参
                order_num = __order_num(user_id=user.user_id, package_id=package_id)
                session.add(Order(order_num=order_num,
                                  user_id=user.user_id, package_id=package_id,
                                  order_status=0, order_package_num=1, address_id=address_result.one().id))
                session.add(BalanceRecord(record_num=__record_num(user_id=user.user_id, record_type=1), bean_num=1, record_type=1, order_num=order_num, user_id=user.user_id))

    result = handler_commit(session)
    return result[0]


def __order_num(package_id=12345, user_id=56789):
    # 商品id后2位+下单时间的年月日12+用户2后四位+随机数4位
    local_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))[2:]
    result = str(package_id)[-2:] + local_time + str(user_id)[-2:] + str(random.randint(1000, 9999))
    return result


def __record_num(record_type=1, user_id=56789):
    # 类型+下单时间的年月日12+用户2后四位+随机数4位
    local_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))[2:]
    result = str(record_type) + local_time + str(user_id)[-2:] + str(random.randint(1000, 9999))
    return result



