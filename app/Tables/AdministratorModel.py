#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/9/4 14:22
"""
from sqlalchemy import (Column, Integer, String, ForeignKey)
from sqlalchemy.orm import relationship
from app.framework_api import date_time
from app.services import ModelBase
from RoleManage import Role
# <-元类


class Administrator(ModelBase):
    __tablename__ = "administrator"
    id = Column(Integer, primary_key=True)
    account = Column(String(length=30), unique=True)
    password = Column(String(length=128), nullable=False)
    enable = Column(Integer)
    cate_time = Column(String(length=50), default=date_time())
    role_type = Column(Integer, ForeignKey('t_roles.role_id'), primary_key=True)
    role = relationship(Role)

    def __init__(self, account, password, role_type=2, enable=0):
        self.account = account
        self.password = password
        self.role_type = role_type
        self.enable = enable

    def to_json(self):
        return {
            'id': self.id,
            'account': self.account,
            'password': self.password,
            'role_type': self.role_type,
            'role': self.role.name,
            'enable': self.enable,
            'cate_time': self.cate_time
        }

    def __repr__(self):
        return "<id={},account={},enable={}>".format(self.id, self.account, self.enable)