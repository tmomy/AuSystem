#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/6/30 11:16
"""

from app.untils import get_params
from app.framework_api import route, build_ret, get_ret
from app.services.api import RoleService,TableInit


@route("/hello", api="测试", methods=['GET', 'POST'])
def person_register():
    params = get_params()
    if params['rlz'] == "1":
        msg = RoleService.service_init_api()
        return get_ret(msg)
    else:
        msg = RoleService.service_update_api()
        return get_ret(msg)


@route("/hellos2", api="测试", methods=['GET', 'POST'])
def person_register():
    params = get_params()
    TableInit.create_all_table()
    return "helloworld"


@route("/hellos5", api="测试", methods=['GET', 'POST'])
def person_register():
    params = get_params()
    TableInit.drop_all_table()
    return "helloworld"

