#!/usr/bin/env python
# encoding: utf-8
"""
@author: XX
@time: 2017/8/30 14:15
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from app.services import ModelBase
from app.framework_api import date_time


class SPU(ModelBase):
    __tablename__ = "spu"
    __table_args__ = {
        'mysql_auto_increment': '10001'
    }

    spu_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=50))
    slogan = Column(String(length=200))
    origin = Column(String(length=50))
    seller_id = Column(String(length=50))
    storage = Column(Integer)
    create_time = Column(String(length=50), default=date_time())
    category_id = Column(Integer, ForeignKey('category.category_id', ondelete='CASCADE'))

    def __init__(self, name, slogan, origin, seller_id, storage, category_id, create_time=date_time()):
        self.name = name
        self.slogan = slogan
        self.origin = origin
        self.seller_id = seller_id
        self.storage = storage
        self.create_time = create_time
        self.category_id = category_id

    def to_json(self):
        return {
            'spu_id': self.spu_id,
            'name': self.name,
            'slogan': self.slogan,
            'origin': self.origin,
            'seller_id': self.seller_id,
            'storage': self.storage,
            'category_id': self.category_id,
            'create_time': self.create_time
        }

    def __repr__(self):
        return "<spu_id={},name={},slogan={},origin={},storage={},category_id={},create_time={}>".format(self.spu_id,
             self.name, self.slogan, self.origin,self.storage, self.category_id, self.create_time)


class SKU(ModelBase):
    __tablename__ = "sku"
    __table_args__ = {
        'mysql_auto_increment': '10001'
    }

    sku_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=50))
    spu_id = Column(Integer, ForeignKey('spu.spu_id', ondelete='CASCADE'))
    storage = Column(Integer)
    price = Column(Integer)
    pic_url = Column(String(length=100))
    create_time = Column(String(length=50), default=date_time())

    children = relationship("SKUMapAttr")

    def __init__(self, spu_id, name, storage, price, pic_url,  create_time=date_time()):
        self.spu_id = spu_id
        self.name = name
        self.storage = storage
        self.price = price
        self.pic_url = pic_url
        self.create_time = create_time

    def to_json(self):
        return {
            'sku_id': self.sku_id,
            'name': self.name,
            'spu_id': self.spu_id,
            'storage': self.storage,
            'price': self.price,
            'pic_url': self.pic_url,
            'create_time': self.create_time
        }

    def __repr__(self):
        return "<sku_id={},name={},spu_id={},storage={},price={},pic_url={},create_time={}>".format(self.sku_id,
                                                                                                    self.spu_id,
                                                                                                    self.name,
                                                                                          self.storage, self.price,
                                                                                          self.pic_url, self.create_time)


class SKUMapAttr(ModelBase):
    __tablename__ = "sku_map_attr"
    __table_args__ = {
        'mysql_auto_increment': '10001'
    }

    id = Column(Integer, primary_key=True, autoincrement=True)
    sku_id = Column(Integer, ForeignKey('sku.sku_id', ondelete='CASCADE'))
    attr_info_id = Column(Integer, ForeignKey('attr_info.id', ondelete='CASCADE'))

    def __init__(self, sku_id, attr_info_id):
        self.sku_id = sku_id
        self.attr_info_id = attr_info_id

    def to_json(self):
        return {
            'id': self.id,
            'sku_id': self.sku_id,
            'attr_info_id': self.attr_info_id
        }

    def __repr__(self):
        return "<id={},sku_id={},attr_info_id={}>".format(self.id, self.sku_id, self.attr_info_id)



