#!/usr/bin/env python
# encoding: utf-8
"""
@author: XX
@time: 2017/9/4 14:17
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy import DateTime
from app.framework_api import date_time
from app.services import ModelBase


class Package(ModelBase):
    __tablename__ = "package"
    __table_args__ = {
        'mysql_auto_increment': '0000'
    }

    package_id = Column(Integer, primary_key=True, autoincrement=True)
    package_name = Column(String(length=50), nullable=False)
    status = Column(Integer, nullable=False)
    create_time = Column(DateTime, default=date_time())
    effect_time = Column(DateTime, default=date_time())
    brand = Column(String(length=50))
    description = Column(String(length=255))
    detail = Column(String(length=255))
    thumbnail_S = Column(String(length=50))
    thumbnail_L = Column(String(length=50))

    def __init__(self, package_name, status, brand, description, detail, thumbnail_S, thumbnail_L,
                 create_time=date_time(), effect_time=date_time()):
        self.package_name = package_name
        self.status = status
        self.create_time = create_time
        self.effect_time = effect_time
        self.brand = brand
        self.description = description
        self.detail = detail
        self.thumbnail_S = thumbnail_S
        self.thumbnail_L = thumbnail_L

    def to_json(self):
        return {
            'package_id': self.package_id,
            'package_name': self.package_name,
            'status': self.status,
            'create_time': str(self.create_time),
            'effect_time': str(self.effect_time),
            'brand': self.brand,
            'description': self.description,
            'detail': self.detail,
            'thumbnail_S': self.thumbnail_S,
            'thumbnail_L': self.thumbnail_L
        }

    def __repr__(self):
        return "<package_id={},package_name={},status={},create_time={},effect_time={},brand={},description={}," \
               "detail={},thumbnail_S={},thumbnail_L={}>".format(
            self.package_id, self.package_name, self.status, self.create_time,self.effect_time, self.brand,
            self.description, self.detail, self.thumbnail_S, self.thumbnail_L)
