#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/8/26 15:18
"""
from sqlalchemy.orm import Session

from app.conf import msg
from app.services.Tables.RoleManage import (RoleRoute, Role, Route)
from app.untils import get_rule_set
from .. import engine, handler_commit

session = Session(engine)


def role_init():
    route_list = []
    rules = get_rule_set()
    for each in rules:
        role, name, rule, func = each
        route = Route(rule, name, *func)
        route_list.append(route)
    return route_list


def db_role_init():
    routes = role_init()
    role_name = "admin"
    session.add_all(routes)
    handler_commit(session.commit())
    role = Role(role_name=role_name)
    for route in routes:
        role.area_set.append(RoleRoute(route))
    session.add(role)
    handler_commit(session.commit())
    return msg.SUCCESS


def db_role_update():
    # 查出已存在的路由
    role_obj = session.query(Role).filter(Role.role_id == 1).one()
    route_list = []
    rule_list = []
    for i in role_obj.area_set:
        route_set = {
            'rule': i.rule,
            'id': i.route_id
        }
        rule_list.append(i.rule)
        route_list.append(route_set)
    # 对当前路由的处理
    rule_now = []
    rules = get_rule_set()
    for each in rules:
        role, name, rule, func = each
        # 新增的路由写入
        if rule not in rule_list:
            role_obj.area_set.append(RoleRoute(Route(rule, name, *func)))
            handler_commit(session.commit())
        rule_now.append(rule)
    # 不存在的路由进行删除
    over_set = set(rule_list) - set(rule_now)
    if len(over_set):
        for de in list(over_set):
            [_db_role_rule_delete(rule_id=s.get('id')) for s in route_list if s.get('rule') == de]
    return msg.SUCCESS


# 新增用户角色
def db_role_add():

    pass


def _db_role_rule_delete(role_id=None, rule_id=None):
    if rule_id:
        rule_del = session.query(Route).filter(Route.route_id == rule_id).one()
        role_rule = session.query(RoleRoute).filter(RoleRoute.route_id == rule_id).one()
        session.delete(rule_del)
        session.delete(role_rule)
    else:
        role_del = session.query(Role).filter(Role.route_id == role_id).one()
        role_rule = session.query(RoleRoute).filter(RoleRoute.role_id == role_id).one()
        session.delete(role_del)
        session.delete(role_rule)
    handler_commit(session.commit())


# 更新字段值
def _field_update(table, field, value=1):
    if not hasattr(table, field):
        return msg.PARAMS_ERR
    setattr(table,field,value)
    return table



