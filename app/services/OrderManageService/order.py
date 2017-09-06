#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2017/8/30 9:18
"""
import time, random
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.Tables.OrderModel import Order
from app.Tables.userModel import User
from app.Tables.PackageModel import Package
from app.Tables.AccountAddress import Address
from .. import engine, handler_commit

session = Session(engine)


# 新增订单
def order_add(params):
    order = Order(order_num=__order_num(user_id=params['user_id']), user_id=params['user_id'], order_status=params['order_status'], order_logistics_company=params['order_logistics_company'], order_logistics_num=params['order_logistics_num'])
    session.add(order)
    result = handler_commit(session)
    return result


# 查询订单
def order_list(cond):

    """
    :info
    @多条件组合查询
    @起始日期有默认值
    :request
    @cond = {
        'order_num': '',
        'login_name': '',
        'order_status': 0,
        'start_time': '2017-08-30 15:04:01',            # 时间区间必须有默认值
        'end_time': '2017-08-30 15:05:13',
        'limit': 10,
        'page': 1,
    }
    :return: result or sql_total
    """
    if cond['login_name']:
        user_id = session.query(User).filter(
            and_(
                User.login_name == cond['login_name']
            )).one().user_id
        cond['user_id'] = user_id
    else:
        cond['user_id'] = ''
    # 缺少收货地址
    sql_result = session.query(Order, User, Package, Address).join(User, isouter=True).join(Package, isouter=True).join(Address, Order.address, isouter=True).filter(
        and_(
            Order.order_num.like('%' + cond['order_num'] + '%') if cond['order_num'] is not None else "",
            Order.user_id.like('%' + cond['user_id'] + '%') if cond['user_id'] is not None else "",
            Order.order_time.between(cond['start_time'], cond['end_time']),
            Order.order_status.like('%' + str(cond['order_status']) + '%') if cond['order_status'] is not None else ""
        ))
    sql_content = sql_result.order_by(Order.order_time).limit(cond['limit']).offset((cond['page']-1)*cond['limit'])
    sql_total = sql_result.count()
    result = [dict(i[0].to_json().items() + {'user_info': i[1].to_json()}.items() + {'package_info': i[2].to_json()}.items() + {'address_info': i[3].to_json()}.items()) for i in sql_content]
    return result, sql_total


# 订单详情
def order_detail(order_num):
    sql_result = session.query(Order, User, Package, Address).join(User, isouter=True).join(Package, isouter=True).join(Address, Order.address, isouter=True).filter(
        and_(
            Order.order_num == order_num
        )).one()
    result = dict(sql_result[0].to_json().items() + {'user_info': sql_result[1].to_json()}.items() + {'package_info': sql_result[2].to_json()}.items() + {'address_info': sql_result[3].to_json()}.items())
    return result


# 修改订单状态
def order_modify_status(cond):
    """
    :info
    @根据订单号修改订单状态
    :request
    @cond = {
        'order_num': '',
        'order_status': 0
    }
    :return: True or False
    """
    order_num = cond['order_num']
    order_status = cond['order_status']
    sql_result = session.query(Order).filter(Order.order_num == order_num).one()
    sql_result.order_status = order_status
    result = handler_commit(session)
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
    order_num = cond['order_num']
    order_logistics_company = cond['order_logistics_company']
    order_logistics_num = cond['order_logistics_num']
    sql_result = session.query(Order).filter(Order.order_num == order_num).one()
    sql_result.order_logistics_company = order_logistics_company
    sql_result.order_logistics_num = order_logistics_num
    result = handler_commit(session)
    return result

def __order_num(package_id=12345, user_id=56789):
    # 商品id后2位+下单时间的年月日12+用户2后四位+随机数4位
    local_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))[2:]
    result = str(package_id)[-2:] + local_time + str(user_id)[-2:] + str(random.randint(1000, 9999))
    return result

