#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/9/8 9:42
"""
from sqlalchemy import (Column, Integer, String, ForeignKey)
from sqlalchemy.orm import relationship
from app.framework_api import date_time
from app.services import ModelBase
# <-元类


class Advise(ModelBase):
    __tablename__ = "advise"
    __table_args__ = {
        'mysql_auto_increment': '0000'
    }
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Integer, nullable=False)
    tel = Column(String(30))
    desc = Column(String(500))
    pics = Column(String(100))
    status = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.user_id'), primary_key=True)
    create_time = Column(String(length=50))

    def __init__(self, advise_type, tel, desc, pics, user_id, status=1):
        self.type = advise_type
        self.tel = tel
        self.desc = desc
        self.pics = str(pics)
        self.user_id = user_id
        self.status = status
        self.create_time = date_time()

    def to_json(self):

        return {
            'id': self.id,
            'type': self.type,
            'tel': self.tel,
            'desc': self.desc,
            'pics': eval(self.pics),
            'status': self.status,
            'user_id': self.user_id,
            'create_time': self.create_time
        }

    def __repr__(self):
        return "<id={},type={},user_id={}>".format(self.id, self.type, self.user_id)
