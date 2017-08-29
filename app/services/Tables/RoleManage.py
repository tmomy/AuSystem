#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/8/25 17:36
"""
# from ..RoleManageService import ModelBase, engine
from sqlalchemy import (Column, Integer, String, DateTime, ForeignKey)
from sqlalchemy.orm import relationship
from app.framework_api import date_time
from app.services import ModelBase, engine
# <-元类

class Role(ModelBase):
    __tablename__ = "t_roles"
    role_id = Column(Integer, primary_key=True)
    name = Column(String(length=30), unique=True)
    enable = Column(Integer)
    cate_time = Column(DateTime, default=date_time())
    area_set = relationship("RoleRoute",cascade="all, delete-orphan", backref='t_roles')

    def __init__(self, role_name, enable=0):
        self.name = role_name
        self.enable = enable

    def to_json(self):
        return {
            'id': self.role_id,
            'name': self.name,
            'enable': self.enable,
            'cate_time': self.cate_time
        }

    def __repr__(self):
        return "<id={},role_name={},enable={}>".format(self.role_id, self.name, self.enable)


class Route(ModelBase):
    __tablename__ = "t_routes"
    route_id = Column(Integer, primary_key=True)
    rule = Column(String(length=255), unique=True)
    name = Column(String(length=30))
    add = Column(Integer, default=-1)
    modify = Column(Integer, default=-1)
    delete = Column(Integer, default=-1)
    search = Column(Integer, default=-1)

    def __init__(self, rule, name, *args):
        self.rule = rule
        self.name = name
        if "add" in args:
            self.add = 0
        if "modify" in args:
            self.modify = 0
        if "delete" in args:
            self.delete = 0
        if "search" in args:
            self.search = 0

    def to_json(self):
        return {
            'id': self.route_id,
            'rule': self.rule,
            'name': self.name,
            'add': self.add,
            'modify': self.modify,
            'delete': self.delete,
            'search': self.search
        }

    def __repr__(self):
        return "<id={},rule={},name={},add={},modify={},delete={},search={}>".format(self.route_id, self.rule, self.name,
                                                                                     self.add, self.modify, self.delete,
                                                                                     self.search)


class RoleRoute(ModelBase):
    __tablename__ = "role_pk_route"
    roles_id = Column(Integer, ForeignKey('t_roles.role_id'), primary_key=True)
    route_id = Column(Integer, ForeignKey('t_routes.route_id'), primary_key=True)
    route_name = Column(String(length=30))
    rule = Column(String(length=255))

    def __init__(self, route):
        self.route = route
        self.rule = route.rule
        self.route_name = route.name
    route = relationship(Route)

