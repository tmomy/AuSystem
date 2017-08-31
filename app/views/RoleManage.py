#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/8/30 10:45
"""
from app.untils import get_params
from app.framework_api import route, build_ret, get_ret
from app.services.api import RoleService,TableInit


@route("/admin/role/operation", api="角色管理", methods=['GET', 'POST'])
def person_register():
    params = get_params()
    opr = params['opr']
    data = params['data']
    if opr == "add":
        resp = RoleService.role_create_api(data['role_name'])
        if resp:
            return build_ret(success=True,msg="创建成功")
        else:
            return build_ret(success=False, msg="角色名已存在!")
    elif opr == "modify":
        resp = RoleService.role_edit_api(data['role_id'], data['role_name'], data['enable'])
        if resp:
            return build_ret(success=True,msg="编辑成功！")
        else:
            return build_ret(success=False, msg="角色名已存在!")
    elif opr == "delete":
        role_id =data['role_id']
        resp, msg = RoleService.role_del_api(role_id)
        return get_ret(error=msg)

    elif opr == "search":
        role_id = data.get('role_id')
        page = data.get('page')
        limit = data.get('limit')
        if not role_id:
            role_id = None
        result, total = RoleService.role_search_api(role_id, page, limit)
        return build_ret(success=True, total=total, data=result)


@route("/admin/role/relationship", api="角色管理", methods=['GET', 'POST'])
def person_register():
    params = get_params()
    opr = params['opr']
    data = params['data']
    if opr == "add":
        role_id = data['role_id']
        rule_list = data['rule_id']
        _, msg = RoleService.relationship_add_api(role_id=role_id, rule_list=rule_list)
        return get_ret(msg)
    elif opr == "delete":
        ids = data['ids']
        _, msg = RoleService.relationship_del_api(id_list=ids)
        return get_ret(msg)
    elif opr == "search":
        role_id = data['role_id']
        route_id = data['route_id']
        total, result = RoleService.relationship_search_api(role_id=role_id, route_id=route_id)
        if total:
            return build_ret(success=True, total=total, data=result)
        else:
            return get_ret(result)
