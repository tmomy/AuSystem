#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/9/1 16:00
"""
from app.untils import get_params
from app.framework_api import route, build_ret, get_ret
from app.services.api import SystemService,TableInit


@route("/admin/system/operation", api="系统初始化操作", methods=['GET', 'POST'])
def role_manage():
    params = get_params()
    opr = params['opr']
    if opr == "add":
        _, result = TableInit.create_all_table()
        return get_ret(result)
    elif opr == "delete":
        _, result = TableInit.drop_all_table()
        return get_ret(result)
    else:
        return build_ret(success=True, msg="该接口还未开放！", code=404)


@route("/admin/system/role", api="系统初始化操作", methods=['GET', 'POST'])
def role_manage():
    params = get_params()
    opr = params['opr']
    if opr == "add":
        _, result = SystemService.service_init_api()
        return get_ret(result)
    elif opr == "modify":
        _, result = SystemService.service_update_api()
        return get_ret(result)
    else:
        return build_ret(success=True, msg="该接口还未开放！", code=404)


@route("/admin/system/rule", api="系统初始化操作", methods=['GET', 'POST'])
def role_manage():
    params = get_params()
    opr = params['opr']
    if opr == "modify":
        _, result = SystemService.rule_enable_api()
        return get_ret(result)
    else:
        return build_ret(success=True, msg="该接口还未开放！", code=404)