#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/9/5 14:34
"""
from app.untils import get_params
from app.framework_api import route, build_ret, get_ret
from app.services.api import AccountService


@route("/account/address/operation", api="系统初始化操作", methods=['GET', 'POST'])
def role_manage():
    params = get_params()
    opr = params['opr']
    if opr == "add":
        address_info = params['data']
        _, result = AccountService.address_add_api(address_info=address_info)
        return get_ret(result)
    elif opr == "search":
        data = params['data']
        page = data.get('page')
        limit = data.get('limit')
        cond = data.get('cond')
        login_name = cond.get('login_name').strip()
        total, result = AccountService.address_search_api(login_name=login_name, page=page, limit=limit)
        if total is not False:
            return build_ret(success=True, total=total, data=result)
        else:
            return get_ret(result)
    else:
        return build_ret(success=True, msg="该接口还未开放！", code=404)