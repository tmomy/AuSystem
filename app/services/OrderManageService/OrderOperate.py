#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2017/8/30 9:18
"""
import time, random, datetime
from app.framework_api import date_time
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.Tables.OrderModel import Order
from app.Tables.userModel import User
from app.Tables.PackageModel import Package
from app.Tables.AccountAddress import Address
from .. import engine, handler_commit
from app.conf.config import web

session = Session(engine)


# 新增订单
# def order_add(params):
#     order = Order(order_num=__order_num(user_id=params['user_id']), user_id=params['user_id'], order_status=params['order_status'], order_logistics_company=params['order_logistics_company'], order_logistics_num=params['order_logistics_num'])
#     session.add(order)
#     result = handler_commit(session)
#     return result


# 查询订单
def order_list(data):

    """
    :info
    @多条件组合查询
    @起始日期有默认值
    :request
    @cond = {
        'cond':{
            'order_num': '',
            'login_name': '',
            'order_status': 0,
            'start_time': '2017-08-30 15:04:01',            # 时间区间必须有默认值
            'end_time': '2017-08-30 15:05:13'
        },
        'limit': 10,
        'page': 1
    }
    :return: result or sql_total
    """
    cond = data['cond']
    if cond['login_name']:
        user_id = session.query(User).filter(
            and_(
                User.login_name == cond['login_name']
            )).one().user_id
        cond['user_id'] = user_id
    else:
        cond['user_id'] = ''
    sql_result = session.query(Order, User, Package, Address).join(User, isouter=True).join(Package, isouter=True).join(Address, Order.address, isouter=True).filter(
        and_(
            Order.order_num.like('%' + str(cond['order_num']) + '%') if cond['order_num'] is not None else "",
            Order.user_id.like('%' + str(cond['user_id']) + '%') if cond['user_id'] is not None else "",
            Order.order_time.between(cond['start_time'], cond['end_time']),
            Order.order_status.like('%' + str(cond['order_status']) + '%') if cond['order_status'] is not None else ""
        ))
    sql_content = sql_result.order_by(Order.order_time).limit(data['limit']).offset((data['page']-1)*data['limit'])
    sql_total = sql_result.count()
    result = [dict(i[0].to_json().items() + {'user_info': i[1].to_json()}.items() + {'package_info': i[2].to_json()}.items() + {'address_info': i[3].to_json()}.items()) for i in sql_content]
    handler_commit(session)
    return result, sql_total


# 订单详情
def order_detail(order_num):
    sql_result = session.query(Order, User, Package, Address).join(User, isouter=True).join(Package, isouter=True).join(Address, Order.address, isouter=True).filter(
        and_(
            Order.order_num == order_num
        ))
    if sql_result.count() is 1:
        record = sql_result.one()
        result = dict(record[0].to_json().items() + {'user_info': record[1].to_json()}.items() + {'package_info': record[2].to_json()}.items() + {'address_info': record[3].to_json()}.items())
    else:
        result = False

    return result


# 修改订单状态
def order_modify_status(cond):
    """
    :info
    @根据订单号修改订单状态
    @如果存在退款，需要返还余额
    :request
    @cond = {
        'order_num': '',
        'order_status': 0
    }
    :return: True or False
    """
    try:
        order_num = cond['order_num']
        order_status = cond['order_status']
        sql_result = session.query(Order).filter(Order.order_num == order_num).one()
        sql_result.order_status = order_status
        # 收货操作，记录收货时间
        if order_status is 2:
            sql_result.order_time_complete = date_time()
        result = handler_commit(session)

    except Exception as e:
        result = False

    return result


# 修改订单快递单号
def order_modify_express(cond):
    """
    :info
    @根据订单号修改订单状态
    :request
    @cond = {
        'order_num': '',
        'order_logistics_company': '',
        'order_logistics_num': 0
    }
    :return: True or False
    """
    try:
        order_num = cond['order_num']
        order_logistics_company = cond['order_logistics_company']
        order_logistics_num = cond['order_logistics_num']
        sql_result = session.query(Order).filter(Order.order_num == order_num).one()
        sql_result.order_logistics_company = order_logistics_company
        sql_result.order_logistics_num = order_logistics_num
        # 绑定运单，自动修改订单状态为已发货
        sql_result.order_status = 1
        result = handler_commit(session)
    except Exception as e:
        result = False

    return result


# 生成订单的开关
def order_switch(cond):
    """
    :info
    @24小时操作一次
    @对用户表修改开关状态 0 1 、开 关
    :request
    @cond = {
        'login_name': '15879179253',
        'switch': 0
    }
    :return: True or False
    """
    sql_result = session.query(User).filter(User.login_name == cond['login_name']).one_or_none()
    if sql_result:
        sql_result.switch = cond['switch']
        sql_result.effective_time = (datetime.date.today() + datetime.timedelta(days=web['switch_delay_time'])).strftime('%Y-%m-%d')
        result = handler_commit(session)
    else:
        result = False
    return result




