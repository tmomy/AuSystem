#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/9/1 15:56
"""
import json
from sqlalchemy.orm import Session
from app.Tables.RoleManage import (RoleRoute, Role, Route)
from app.conf import msg, config
from app.untils import get_rule_set
from ..api.RoleService import role_rule_del
from .. import engine, handler_commit, err_logging
from . import redis_service
session = Session(engine)


@err_logging
def db_role_init():
    routes = _role_init()
    role_name = "admin"
    session.add_all(routes)
    handler_commit(session)
    role = Role(role_name=role_name)
    administrator = Role(role_name="administrator")
    user = Role(role_name="user")
    tourists = Role(role_name="tourists")
    for route in routes:
        role.area_set.append(RoleRoute(route))
    session.add_all([role, administrator, user, tourists])
    return handler_commit(session)


@err_logging
def db_role_update():
    # 查出已存在的路由
    role_obj = session.query(Role).filter(Role.role_id == 1).one()
    route_list = []
    rule_list = []
    for role_route in role_obj.area_set:
        route_set = {
            'rule': role_route.route.rule,
            'id': role_route.route_id
        }
        rule_list.append(role_route.route.rule)
        route_list.append(route_set)
    # 对当前路由的处理
    rule_now = []
    rules = get_rule_set()
    for each in rules:
        role, name, rule, func = each
        # 新增的路由写入
        if rule not in rule_list:
            role_obj.area_set.append(RoleRoute(Route(rule, name, *func)))
            handler_commit(session)
        rule_now.append(rule)
    # 不存在的路由进行删除
    over_set = set(rule_list) - set(rule_now)
    if len(over_set):
        for de in list(over_set):
            [role_rule_del(rule_id=s.get('id')) for s in route_list if s.get('rule') == de]
    return True, msg.SUCCESS


@err_logging
def sys_enable_rule():
    roles = session.query(Role).all()
    if not len(roles):
        return False, msg.ERROR(1, "数据库无管理员数据！")
    for role in roles:
        role_dict = role.to_json()
        re_role = _rule_collect(role,role_dict)
        print role.role_id
        print re_role
        redis_key = config.web['rule_redis_pix'] + str(role.role_id)
        print redis_key
        redis_service.set(redis_key, json.dumps(re_role))
    return True, msg.SUCCESS

    pass


def _rule_collect(role, role_dict):
    rule_list = role.area_set
    for field in config.web['opr']:
        role_dict[field] = []
    for role_route in rule_list:
        search_route = role_route.route
        for opr in config.web['opr']:
            if getattr(search_route, opr) or getattr(role_route, opr):
                role_dict[opr].append(search_route.rule)
            else:
                pass
    return role_dict


def _role_init():
    route_list = []
    rules = get_rule_set()
    for each in rules:
        role, name, rule, func = each
        route = Route(rule, name, func)
        route_list.append(route)
    return route_list
