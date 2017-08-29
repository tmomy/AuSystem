#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2017/8/29 14:56
"""
from sqlalchemy import (Column, Integer, String, DateTime, ForeignKey)
from sqlalchemy.orm import relationship
from app.framework_api import date_time
from app.services import ModelBase
# <-元类

class User(ModelBase):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, unique=True,
                       nullable=False, default=10000)
    login_name = Column(String(length=30), unique=True, nullable=False)
    login_pass = Column(String(length=128), nullable=False)
    rest_day = Column(Integer, default=0)
    user_integral = Column(Integer, default=0)
    name = Column(String(length=30))
    nick_name = Column(String(length=30))
    sex = Column(String(length=30))
    birthday = Column(String(length=30))
    address_province = Column(String(length=30))
    address_city = Column(String(length=30))
    tel = Column(String(length=30))
    e_mail = Column(String(length=30))
    register_time = Column(DateTime, default=date_time())
    # area_set = relationship("RoleRoute",cascade="all, delete-orphan", backref='t_roles')

    def __init__(self, login_name, login_pass, rest_day, user_integral, name=None, nick_name=None, sex=None, birthday=None, tel=None, e_mail=None, address_province=None, address_city=None):
        self.login_name = login_name
        self.login_pass = login_pass
        self.rest_day = rest_day
        self.user_integral = user_integral
        self.name = name
        self.nick_name = nick_name
        self.sex = sex
        self.birthday = birthday
        self.tel = tel
        self.e_mail = e_mail
        self.address_province = address_province
        self.address_city = address_city

    def to_json(self):
        return {
            'login_name': self.login_name,
            'login_pass': self.login_pass,
            'rest_day': self.rest_day,
            'user_integral': self.user_integral,
            'name': self.name,
            'nick_name': self.nick_name,
            'sex': self.sex,
            'tel': self.tel,
            'birthday': self.birthday,
            'e_mail': self.e_mail,
            'address_province': self.address_province,
            'address_city': self.address_city,
        }

    def __repr__(self):
        return "<user_id={},login_name={},login_pass={}>".format(self.user_id, self.login_name, self.login_pass)

