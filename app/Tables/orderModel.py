#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2017/8/25 17:36
"""
from sqlalchemy import (Column, Integer, String, DateTime, ForeignKey)
from sqlalchemy.orm import relationship
from app.framework_api import date_time
from app.services import ModelBase
# <-元类

class Order(ModelBase):
    __tablename__ = "order"

    order_id = Column(Integer, primary_key=True, autoincrement=True)
    order_num = Column(String(length=30), primary_key=True, unique=True, nullable=False)
    order_status = Column(Integer, default=0)         # 0/1/2/3/4 待发货，已发货，已收货，拒收货，交易关闭
    order_logistics_company = Column(String(length=30))
    order_logistics_num = Column(String(length=30))
    # package_id = Column(Integer, ForeignKey('package.package_id'))
    # user_id = Column(Integer, ForeignKey('user.user_id'))
    order_time = Column(DateTime, default=date_time())


    def __init__(self, order_num, order_status, order_logistics_company, order_logistics_num, package_id=None, user_id=None):
        self.order_num = order_num
        self.order_status = order_status
        self.order_logistics_company = order_logistics_company
        self.order_logistics_num = order_logistics_num
        # self.package_id = package_id
        # self.user_id = user_id
        self.order_time = date_time()
        print self.to_json()


    def to_json(self):
        return {
            'order_num': self.order_num,
            'order_status': self.order_status,
            'order_logistics_company': self.order_logistics_company,
            'order_logistics_num': self.order_logistics_num,
            # 'package_id': self.package_id,
            # 'user_id': self.user_id,
            'order_time': str(self.order_time)
        }

    def __repr__(self):
        return "<order_num={},order_status={},order_logistics_company={},order_logistics_num={}>".format(self.order_num, self.order_status, self.order_logistics_company, self.order_logistics_num)