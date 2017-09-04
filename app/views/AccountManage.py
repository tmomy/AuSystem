#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/9/4 15:26
"""
from app.untils import get_params
from app.framework_api import route, build_ret, get_ret
from app.services.api import AccountService


@route("/admin/account/operation", api="会员管理操作", methods=['GET', 'POST'])
def account_manage():
    params = get_params()
    opr = params['opr']
    data = params['data']
    if opr == "add":
        _, result = AccountService.admin_account_entry_api(data['account'],effective_time=data['effective_time'],
                                                     rest_day=data['rest_day'], user_integral=data['user_integral'])
        return get_ret(result)
    elif opr == "modify":
        user_id = data.pop('user_id')
        _, result = AccountService.admin_account_edit_api(user_id=user_id, account_info=data)
        return get_ret(result)
    elif opr == "search":
        user_id = data.get('user_id')
        page = data.get('page')
        limit = data.get('limit')
        pass
    else:
        return build_ret(success=True, msg="该接口还未开放！", code=404)