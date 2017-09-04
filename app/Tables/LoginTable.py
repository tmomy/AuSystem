#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/9/4 9:22
"""
from sqlalchemy import (Column, Integer, String, DateTime, ForeignKey)
from sqlalchemy.orm import relationship
from app.framework_api import date_time
from app.services import ModelBase
from userModel import User
# <-元类


class LoginTable(ModelBase):
    __tablename__ = "login_table"
    id = Column(Integer, primary_key=True)
    username = Column(String(length=30), unique=True)
    user_id = Column(Integer, ForeignKey('user.user_id'), primary_key=True)
    enable = Column(Integer)
    create_time = Column(String(length=50), default=date_time())
    expires = Column(DateTime)

    def __init__(self, username, user, expires=date_time()):
        self.username = username
        self.password = user.login_pass
        self.user_id = user.user_id
        self.enable = user.enable
        self.expires = expires

    def to_json(self):
        return {
            'id': self.id,
            'username': self.name,
            'create_time': self.cate_time,
            'expires': self.expires
        }

    user = relationship(User)