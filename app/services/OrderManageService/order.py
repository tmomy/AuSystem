#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2017/8/30 9:18
"""
import time, random
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.Tables.orderModel import Order
from app.conf import msg
from app.untils import get_rule_set
from .. import engine, handler_commit

session = Session(engine)

# 新增订单

def order_add():

    order = Order(order_num=_order_num(), order_status=0, order_logistics_company='0', order_logistics_num='0')
    session.add(order)
    result = handler_commit(session)
    return result

# 查询订单
def order_list():
    cond = {
        'order_num': '',
        'user_id': '',
        'order_status': 0,
        'start_time': '2017-08-30 15:04:01',            # 时间区间必须有默认值
        'end_time': '2017-08-30 15:05:13',
        'limit': 10,
        'page': 1,
    }
    sql_result = session.query(Order).filter(
        and_(
            Order.order_num.like('%' + cond['order_num'] + '%') if cond['order_num'] is not None else "",
            # Order.user_id.like('%' + cond['user_id'] + '%') if cond['user_id'] is not None else "",
            Order.order_time.between(cond['start_time'], cond['end_time']),
            Order.order_status.like('%' + str(cond['order_status']) + '%') if cond['order_status'] is not None else ""
        ))
    sql_content = sql_result.order_by(Order.order_time).limit(cond['limit']).offset((cond['page']-1)*cond['limit'])
    sql_total = sql_result.count()
    result = [i.to_json() for i in sql_content]
    return result, sql_total


# 修改订单状态
def order_modify(order_num='45170830150453899582', order_status=1):
    sql_result = session.query(Order).filter(Order.order_num == order_num).one()
    sql_result.order_status = order_status
    result = handler_commit(session)
    return result


def _order_num(package_id=12345, user_id=56789):
    # 商品id后2位+下单时间的年月日12+用户2后四位+随机数4位
    local_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))[2:]
    result = str(package_id)[-2:] + local_time + str(user_id)[-2:] + str(random.randint(1000, 9999))
    return result

# if __name__ == '__main__':
    # _order_num()