#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/8/26 15:18
"""
from sqlalchemy.orm import Session
from app.Tables.RoleManage import (RoleRoute, Role, Route)
from app.conf import msg, config
from .. import (engine, handler_commit, err_logging, sys_logging, field_update)
import traceback
session = Session(engine)


# role add
def db_role_add(role, enable):
    new_role = Role(role_name=role, enable=enable)
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
    return db_role_rule_delete(role_id=role_id)


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
        result = session.query(Role).filter(Role.role_id == role_id).one_or_none()
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
        del_rule = session.query(RoleRoute).filter(RoleRoute.id == rule_id).one_or_none()
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
def db_relationship_edit(rule_id, edit_info):
    rel_ship = session.query(RoleRoute).filter(RoleRoute.id == rule_id).one_or_none()
    re_bool = True
    re_msg = msg.SUCCESS
    if not rel_ship:
        return False, msg.ERROR(1, "系统不存在该权限！")
    rel_info = rel_ship.to_json()
    for field, value in edit_info.items():
        if value not in [0,1]:
            return False, msg.ERROR(1, "输入超出限定范围！")
        if rel_info[field] == 1:
            re_bool = True
            re_msg = msg.ERROR(0,"该权限已被系统设定为禁用，当前操作可能无效！")
        edit_result = field_update(rel_ship, field,value)
        if not edit_result:
            re_bool = False
            re_msg = msg.ERROR(1, "输入字段不存在！")
            return re_bool, re_msg
    session.flush()
    handler_commit(session)
    return re_bool, re_msg


def db_route_search(route_id, role_id, page=1, limit=10):
    offset = (page - 1) * limit
    data = []
    total = 0
    if route_id:
        search_route = session.query(Route).filter(Route.route_id == route_id).one_or_none()
        if search_route:
            total = 1
            data.append(search_route.to_json())
    else:
        if role_id:
            search_role = session.query(RoleRoute).filter(RoleRoute.role_id == role_id).all()
            if not len(search_role):
                return False, msg.ERROR(1,"角色不存在！")
            ids = [_id.route_id for _id in search_role]
        else:
            ids = []
        search_route = session.query(Route).filter(~Route.route_id.in_(ids)).order_by(Route.route_id)
        total = search_route.count()
        print total
        for each in search_route.offset(offset).limit(limit):
            data.append(each.to_json())
    return total, data


@err_logging
def db_route_edit(route_id, edit_info):
    search_route = session.query(Route).filter(Route.route_id == route_id).one_or_none()
    if not search_route:
        return False, msg.ERROR(1, "该路由不存在！")
    for field, value in edit_info.items():
        if field not in ["name"] and value not in [0, 1]:
                return False, msg.ERROR(1, "输入超出限定范围！")
        edit_result = field_update(search_route,field,value)
        if not edit_result:
            return False, msg.ERROR(1,"输入字段不存在！")
    return handler_commit(session)


# delete role or rule
def db_role_rule_delete(role_id=None, rule_id=None):
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




