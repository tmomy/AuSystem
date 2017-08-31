#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/8/26 15:18
"""
from sqlalchemy.orm import Session
from sqlalchemy import update, desc, and_
from app.Tables.RoleManage import (RoleRoute, Role, Route)
from app.conf import msg
from app.untils import get_rule_set
from .. import engine, handler_commit, err_logging, sys_logging
import traceback
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
    handler_commit(session)
    role = Role(role_name=role_name)
    administrator = Role(role_name="administrator")
    user = Role(role_name="user")
    for route in routes:
        role.area_set.append(RoleRoute(route))
    session.add_all([role, administrator, user])
    handler_commit(session)
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
            handler_commit(session)
        rule_now.append(rule)
    # 不存在的路由进行删除
    over_set = set(rule_list) - set(rule_now)
    if len(over_set):
        for de in list(over_set):
            [_db_role_rule_delete(rule_id=s.get('id')) for s in route_list if s.get('rule') == de]
    return msg.SUCCESS


# role add
def db_role_add(role):
    new_role = Role(role_name=role)
    session.add(new_role)
    return handler_commit(session)


# role modify
def db_role_modify(role_id,role_name,enable):
    try:
        session.query(Role).filter(Role.role_id == role_id).\
            update({Role.name: role_name, Role.enable: enable}, synchronize_session=False)
        return handler_commit(session)
    except:
        sys_logging.debug("mysql.err:{}".format(traceback.format_exc()))
        return False, msg.ERROR(1, "编辑失败！")


@err_logging
def db_role_del(role_id):
    if role_id in [1, 2, 3]:
        return False, msg.ERROR(1,"该角色不能删除！")
    return _db_role_rule_delete(role_id=role_id)


@err_logging
def db_role_search(role_id=None, page=1, limit=10):
    offset = (page - 1) * limit
    data = []
    if not role_id:
        result = session.query(Role).order_by(Role.role_id)
        for each in result.offset(offset).limit(limit):
            data.append(each.to_json())
        total = result.count()
    else:
        result = session.query(Role).filter(Role.role_id == role_id).one()
        data.append(result.to_json())
        total = 1
    return data, total


@err_logging
def db_relationship_add(role_id, rule_list):
    pending_role = session.query(Role).filter(Role.role_id == role_id).one_or_none()
    if not pending_role:
        return False, msg.ERROR(1, "角色不存在！")
    for rule in pending_role.area_set:
        if rule.route_id in rule_list:
            return False, msg.ERROR(1, "权限已经拥有!")
    for rule_id in rule_list:
        rule = session.query(Route).filter(Route.route_id == rule_id).one_or_none()
        if not rule:
            return False, msg.ERROR(1, "输入权限不存在！")
        new_rule = RoleRoute(rule)
        pending_role.area_set.append(new_rule)
    return handler_commit(session)


@err_logging
def db_relationship_del(id_list):
    if not id_list:
        return False, msg.ERROR(1, "输入为空!")
    for rule_id in id_list:
        print 111
        del_rule = session.query(RoleRoute).filter(RoleRoute.id == rule_id).one_or_none()
        print del_rule, 1
        if not del_rule:
            return False, msg.ERROR(1, "操作中有不存在的权限!")
        session.delete(del_rule)
    return handler_commit(session)


@err_logging
def db_relationship_search(role_id=None,route_id=None, page=1, limit=10):
    offset = (page - 1) * limit
    data = []
    if role_id:
        search_filter = RoleRoute.role_id == role_id
    else:
        search_filter = RoleRoute.route_id == route_id
    search_rule = session.query(RoleRoute).filter(search_filter).order_by(RoleRoute.id)
    total = search_rule.count()
    if total:
        for rule in search_rule.offset(offset).limit(limit):
            data.append(rule.to_json())
    return total, data

@err_logging
def db_relationship_edit():
    pass






# delete role or rule
def _db_role_rule_delete(role_id=None, rule_id=None):
    if rule_id:
        rule_del = session.query(Route).filter(Route.route_id == rule_id).one_or_none()
        if not rule_del:
            return False, msg.ERROR(1, "该权限不存在！")
        role_rule = session.query(RoleRoute).filter(RoleRoute.route_id == rule_id).all()
        session.delete(rule_del)
    else:
        role_del = session.query(Role).filter(Role.role_id == role_id).one_or_none()
        if not role_del:
            return False, msg.ERROR(1, "该角色不存在！")
        role_rule = session.query(RoleRoute).filter(RoleRoute.role_id == role_id).all()
        session.delete(role_del)
    for each in role_rule:
        session.delete(each)
    return handler_commit(session)


# 更新字段值
def _field_update(table, field, value=1):
    if not hasattr(table, field):
        return msg.PARAMS_ERR
    setattr(table,field,value)
    return table


