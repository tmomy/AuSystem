#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2017/8/29 14:56
"""
from sqlalchemy import (Column, Integer, String, Date, ForeignKey)
from sqlalchemy.orm import relationship
from app.framework_api import date_time
from app.services import ModelBase
# <-元类


class User(ModelBase):
    __tablename__ = "user"
    __table_args__ = {
        'mysql_auto_increment': '10001'
    }

    user_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    login_name = Column(String(length=30), unique=True, nullable=False)
    login_pass = Column(String(length=128), default="")
    rest_day = Column(Integer, default=0)
    role_type = Column(Integer)
    enable = Column(Integer,default=0)
    user_integral = Column(Integer, default=0)
    name = Column(String(length=30), default="")
    nick_name = Column(String(length=30), default="")
    sex = Column(String(length=30), default="")
    birthday = Column(String(length=30), default="")
    address_province = Column(String(length=30), default="")
    address_city = Column(String(length=30), default="")
    tel = Column(String(length=30), default="")
    e_mail = Column(String(length=30), default="")
    effective_time = Column(Date, nullable=False)  # 生效时间
    register_time = Column(String(length=50), default=date_time())

    def __init__(self, login_name=None,role_type=None, rest_day=0, user_integral=0, effective_time=0):
        self.login_name = login_name
        self.rest_day = rest_day
        self.role_type = role_type
        self.effective_time = effective_time
        self.user_integral = user_integral
        self.tel = login_name

    def to_json(self):
        return {
            'user_id': self.user_id,
            'login_name': self.login_name,
            'rest_day': self.rest_day,
            "enable": self.enable,
            'user_integral': self.user_integral,
            'name': self.name,
            'nick_name': self.nick_name,
            'sex': self.sex,
            'tel': self.tel,
            'birthday': self.birthday,
            'e_mail': self.e_mail,
            'effective_time': str(self.effective_time),
            'address_province': self.address_province,
            'address_city': self.address_city,
        }

    def __repr__(self):
        return "<user_id={},login_name={}".format(self.user_id, self.login_name)

