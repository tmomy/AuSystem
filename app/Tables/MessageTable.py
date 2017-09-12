#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/9/8 15:01
"""
from sqlalchemy import (Column, Integer, String, ForeignKey)
from sqlalchemy.orm import relationship
from app.framework_api import date_time
from app.services import ModelBase
# <-元类


class Message(ModelBase):
    __tablename__ = "message"
    __table_args__ = {
        'mysql_auto_increment': '0000'
    }
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Integer, nullable=False)  # 0/1 广播、私信
    desc = Column(String(100))
    waiter_id = Column(Integer)
    reply_id = Column(Integer)
    pic = Column(String(30))
    detail = Column(String(200))
    user_id = Column(Integer, ForeignKey('user.user_id'), primary_key=True)
    create_time = Column(String(length=50))

    def __init__(self, waiter_id, message_type, detail, user_id, desc="", pic="", reply_id=""):
        self.waiter_id = waiter_id
        self.type = message_type
        self.detail = detail
        self.user_id = user_id
        self.reply_id = reply_id
        self.desc = desc
        self.pic = pic
        self.create_time = date_time()

    def to_json(self):
        return {
            'id': self.id,
            'type': self.type,
            'detail': self.detail,
            'waiter_id': self.waiter_id,
            'reply_id': self.reply_id,
            'user_id': self.user_id,
            'desc': self.desc,
            'pic': self.pic,
            'create_time': self.create_time
        }

    def __repr__(self):
        return "<id={},type={},user_id={}>".format(self.id, self.type, self.user_id)