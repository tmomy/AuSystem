#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/8/25 17:36
"""
from sqlalchemy import (Column, Integer, String, ForeignKey)
from sqlalchemy.orm import relationship
from app.framework_api import date_time
from app.services import ModelBase
# <-元类


class Role(ModelBase):
    __tablename__ = "t_roles"
    role_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=30), unique=True)
    enable = Column(Integer)
    create_time = Column(String(length=50), default=date_time())
    area_set = relationship("RoleRoute",cascade="save-update, delete", backref='t_roles')

    def __init__(self, role_name, enable=0):
        self.name = role_name
        self.enable = enable

    def to_json(self):
        return {
            'id': self.role_id,
            'name': self.name,
            'enable': self.enable,
            'create_time': self.create_time
        }

    def __repr__(self):
        return "<id={},role_name={},enable={}>".format(self.role_id, self.name, self.enable)


class Route(ModelBase):
    __tablename__ = "t_routes"
    route_id = Column(Integer, primary_key=True, autoincrement=True)
    rule = Column(String(length=255), unique=True)
    name = Column(String(length=30))
    add = Column(Integer, default=-1)
    modify = Column(Integer, default=-1)
    delete = Column(Integer, default=-1)
    search = Column(Integer, default=-1)

    def __init__(self, rule, name, opr):
        status = 1
        self.rule = rule
        self.name = name
        if "add" in opr:
            self.add = status
        if "modify" in opr:
            self.modify = status
        if "delete" in opr:
            self.delete = status
        if "search" in opr:
            self.search = status

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
    id = Column(Integer, primary_key=True, autoincrement=True)
    role_id = Column(Integer, ForeignKey('t_roles.role_id'), primary_key=True)
    route_id = Column(Integer, ForeignKey('t_routes.route_id'), primary_key=True)
    add = Column(Integer, default=-1)
    modify = Column(Integer, default=-1)
    delete = Column(Integer, default=-1)
    search = Column(Integer, default=-1)

    def __init__(self, route):
        self.modify = route.modify
        self.search = route.search
        self.delete = route.delete
        self.route = route
        self.add = route.add

    def to_json(self):
        return {
            'id': self.id,
            'route_id': self.route_id,
            'role_id': self.role_id,
            'rule': self.route.rule,
            'name': self.route.name,
            'role': self.role.name,
            'add': self.add,
            'modify': self.modify,
            'delete': self.delete,
            'search': self.search
        }
    route = relationship(Route)
    role = relationship(Role)


