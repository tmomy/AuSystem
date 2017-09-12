#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2017/8/25 17:36
"""
from sqlalchemy import (Column, Integer, String, DateTime, ForeignKey)
from sqlalchemy.orm import relationship
from app.framework_api import date_time
from app.Tables.AccountAddress import Address
from app.services import ModelBase
# <-元类

class Order(ModelBase):
    __tablename__ = "order"

    order_id = Column(Integer, primary_key=True, autoincrement=True)
    order_num = Column(String(length=30), primary_key=True, unique=True, nullable=False)
    order_package_num = Column(Integer, nullable=False)
    order_status = Column(Integer, default=0)         # 0/1/2/3/4 待发货，已发货，已收货，拒收货，交易关闭
    order_logistics_company = Column(String(length=30))
    order_logistics_num = Column(String(length=30))

    order_time = Column(DateTime, default=date_time())
    order_time_complete = Column(DateTime)
    package_id = Column(Integer, ForeignKey('package.package_id'))
    user_id = Column(Integer, ForeignKey('user.user_id'))
    address_id = Column(Integer, ForeignKey('address.id'))


    def __init__(self, order_num, order_package_num, address_id,order_time_complete=None, order_status=0, order_logistics_company=None, order_logistics_num=None, package_id=None, user_id=None):
        self.order_num = order_num
        self.order_package_num = order_package_num
        self.order_status = order_status
        self.order_logistics_company = order_logistics_company
        self.order_logistics_num = order_logistics_num
        self.package_id = package_id
        self.user_id = user_id
        self.address_id = address_id
        self.order_time = date_time()
        self.order_time_complete = order_time_complete


    def to_json(self):
        return {
            'order_num': self.order_num,
            'order_package_num': self.order_package_num,
            'order_status': self.order_status,
            'order_logistics_company': self.order_logistics_company,
            'order_logistics_num': self.order_logistics_num,
            'package_id': self.package_id,
            'user_id': self.user_id,
            'address_id': self.address_id,
            'order_time': str(self.order_time),
            'order_time_complete': str(self.order_time_complete)
        }

    def __repr__(self):
        return "<order_num={},order_status={},order_logistics_company={},order_logistics_num={}>".format(self.order_num, self.order_status, self.order_logistics_company, self.order_logistics_num)

    address = relationship("Address")


# 余额明细记录表
class BalanceRecord(ModelBase):
    __tablename__ = "balance_record"

    record_id = Column(Integer, primary_key=True, autoincrement=True)
    record_num = Column(String(length=30), primary_key=True, unique=True, nullable=False)
    bean_num = Column(Integer, nullable=False)
    record_type = Column(Integer)       # 0充值1扣费
    record_time = Column(DateTime, default=date_time())
    order_num = Column(String(length=30), ForeignKey('order.order_num'))
    user_id = Column(Integer, ForeignKey('user.user_id'))


    def __init__(self, record_num, bean_num, record_type, order_num=None, user_id=None):
        self.record_num = record_num
        self.bean_num = bean_num
        self.record_type = record_type
        self.order_num = order_num
        self.user_id = user_id


    def to_json(self):
        return {
            'record_num': self.record_num,
            'bean_num': self.bean_num,
            'record_type': self.record_type,
            'order_num': self.order_num,
            'user_id': self.user_id,
            'record_time': str(self.record_time)
        }

    def __repr__(self):
        return "<record_num={},bean_num={},record_type={}>".format(self.record_num, self.bean_num, self.record_type)