#!/usr/bin/env python
# encoding: utf-8
"""
@author: XX
@time: 2017/9/1 10:33
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from app.services import ModelBase
from sqlalchemy.orm import relationship, backref


class Category(ModelBase):
    __tablename__ = "category"
    __table_args__ = {
        'mysql_auto_increment': '1'
    }

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=50))
    parent_id = Column(Integer, ForeignKey(category_id))
    sn = Column(Integer)
    children = relationship("Category", cascade="all,delete-orphan", backref=backref("parent", remote_side=category_id))

    def __init__(self, name, parent_id, sn):
        self.name = name
        self.parent_id = parent_id
        self.sn = sn

    def to_json(self):
        return {
            'category_id': self.category_id,
            'name': self.name,
            'parent_id': self.parent_id,
            'sn': self.sn
        }

    def __repr__(self):
        return "<category_id={},name={},parent_id={},sn={}>".format(
            self.category_id, self.name, self.parent_id, self.sn)
