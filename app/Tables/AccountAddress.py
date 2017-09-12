#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/9/5 11:33
"""
from sqlalchemy import (Column, Integer, String, DateTime, ForeignKey)
from sqlalchemy.orm import relationship
from app.framework_api import date_time
from app.services import ModelBase
from userModel import User
# <-元类


class Address(ModelBase):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.user_id'), primary_key=True)
    login_name = Column(String(length=30), default="")
    tag = Column(String(length=30), unique=True)
    detail = Column(String(length=100), default="")
    default = Column(Integer, default=1)
    create_time = Column(String(length=50))
    province = Column(String(length=30), default="")
    city = Column(String(length=30), default="")
    area = Column(String(length=150), default="")
    addressee = Column(String(length=30), default="")
    tel = Column(String(length=30), default="")

    def __init__(self, user):
        self.user_id = user.user_id
        self.login_name = user.login_name
        self.create_time = date_time()

    def to_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'login_name': self.login_name,
            'tag': self.tag,
            'detail': self.detail,
            'default': self.default,
            'city': self.city,
            'province': self.province,
            'area': self.area,
            'addressee': self.addressee,
            'tel': self.tel,
            'create_time': self.create_time
        }
    user = relationship(User)
