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

class Task(ModelBase):
    __tablename__ = "task"
    __table_args__ = {
        'mysql_auto_increment': '10001'
    }

    task_id = Column(Integer, primary_key=True)

    task_num = Column(Integer, default=1)
    task_create_time = Column(DateTime, default=date_time())
    task_do_time = Column(DateTime, default=date_time())

    user_id = Column(Integer, ForeignKey('user.user_id'))



    def __init__(self, task_num, task_do_time, user_id=None):
        self.task_num = task_num
        # self.task_type = task_type
        self.task_do_time = task_do_time
        self.user_id = user_id
        self.task_create_time = date_time()

    def to_json(self):
        return {
            'task_id': self.task_id,
            'task_num': self.task_num,
            # 'task_type': self.task_type,
            'user_id': self.user_id,
            'task_do_time': str(self.task_do_time),
            'task_create_time': str(self.task_create_time)
        }

    def __repr__(self):
        return "<task_id={},order_num={},task_do_time={},task_create_time={}>".format(self.task_id,
                                                                                      self.order_num,
                                                                                      self.task_do_time,
                                                                                      self.task_create_time)
