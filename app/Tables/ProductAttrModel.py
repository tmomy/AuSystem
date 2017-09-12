#!/usr/bin/env python
# encoding: utf-8
"""
@author: XX
@time: 2017/8/30 14:48
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from app.services import ModelBase


class AttrCategory(ModelBase):
    __tablename__ = "attr_category"
    __table_args__ = {
        'mysql_auto_increment': '10001'
    }

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=50))

    def __init__(self, name):
        self.name = name

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def __repr__(self):
        return "<id={},name={}>".format(self.id, self.name)


class AttrInfo(ModelBase):
    __tablename__ = "attr_info"
    __table_args__ = {
        'mysql_auto_increment': '10001'
    }

    id = Column(Integer, primary_key=True, autoincrement=True)
    attr_id = Column(Integer, ForeignKey('attr_category.id', ondelete='CASCADE'))
    attr_value = Column(String(length=50))

    def __init__(self, attr_id, attr_value):
        self.attr_id = attr_id
        self.attr_value = attr_value

    def to_json(self):
        return {
            'id': self.id,
            'attr_id': self.attr_id,
            'attr_value': self.attr_value
        }

    def __repr__(self):
        return "<id={},attr_id={},attr_value={}>".format(self.id, self.attr_id, self.attr_value)


class SPUMapAttr(ModelBase):
    __tablename__ = "spu_map_attr"
    __table_args__ = {
        'mysql_auto_increment': '10001'
    }

    id = Column(Integer, primary_key=True, autoincrement=True)
    attr_id = Column(Integer, ForeignKey('attr_category.id', ondelete='CASCADE'))
    spu_id = Column(Integer, ForeignKey('spu.spu_id', ondelete='CASCADE'))

    def __init__(self, attr_id, spu_id):
        self.attr_id = attr_id
        self.spu_id = spu_id

    def to_json(self):
        return {
            'id': self.id,
            'attr_id': self.attr_id,
            'spu_id': self.spu_id
        }

    def __repr__(self):
        return "<id={},attr_id={},spu_id={}>".format(self.id, self.attr_id, self.spu_id)