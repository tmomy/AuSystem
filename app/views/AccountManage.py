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
        account_info = data
        _, result = AccountService.admin_account_entry_api(account_info)
        return get_ret(result)
    elif opr == "modify":
        user_id = data.pop('user_id')
        _, result = AccountService.admin_account_edit_api(user_id=user_id, account_info=data)
        return get_ret(result)
    elif opr == "search":
        page = data.get('page')
        limit = data.get('limit')
        cond = data.get('cond')
        login_name = cond.get('login_name')
        enable = cond.get('enable')
        sort = cond.get('sort')
        if not enable:
            enable = None
        total, data = AccountService.admin_account_search_api(login_name=login_name, enable=enable, page=int(page),
                                                              limit=int(limit), sort=sort)
        if total is not False:
            return build_ret(success=True, total=total, data=data)
        else:
            return get_ret(data)
        pass
    elif opr == "delete":
        user_id = data.get('user_id')
        re_bool, result = AccountService.admin_account_del_api(user_id=user_id)
        return get_ret(result)
    else:
        return build_ret(success=True, msg="该接口还未开放！", code=404)


from app.untils import get_params
from app.framework_api import route, build_ret, get_ret
from app.services.api import AccountService


@route("/admin/administrator/operation", api="系统初始化操作", methods=['GET', 'POST'])
def role_manage():
    params = get_params()
    opr = params['opr']
    data = params['data']
    if opr == "add":
        re_bool, result = AccountService.admin_administrator_add_api(account=data['account'], password=data['password'],
                                                                     role_type=data['role_type'], enable=data['enable'])
        return get_ret(result)
    elif opr == "modify":
        admin_id = data.pop('id')
        re_bool, result = AccountService.admin_administrator_edit_api(admin_id=admin_id, edit_info=data)
        return get_ret(result)
    elif opr == "delete":
        admin_id = data['id']
        re_bool, result = AccountService.admin_administrator_del_api(admin_id=admin_id)
        return get_ret(result)
    elif opr == "search":
        total, result = AccountService.admin_administrator_search_api()
        if total is not False:
            return build_ret(success=True, total=total, data=result)
        else:
            get_ret(result)
    else:
        return build_ret(success=True, msg="该接口还未开放！", code=404)