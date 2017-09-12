#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/9/8 15:38
"""
from app.untils import get_params
from app.framework_api import route, build_ret, get_ret
from app.services.api import AdviseService


@route("/advise/operation", api="反馈意见模块", methods=['GET', 'POST'])
def advise():
    params = get_params()
    opr = params['opr']
    if opr == "add":
        # advise_type, tel, desc, pics
        data = params['data']
        advise_type = data['type']
        tel = data['tel']
        desc = data['desc']
        pics = data['pics']
        re_bool, result = AdviseService.advise_entry_api(advise_type=advise_type, tel=tel, desc=desc, pics=pics)
        return get_ret(result)
    elif opr == "search":
        page = params['data']['page']
        limit = params['data']['limit']
        cond = params['data']['cond']
        user_id = cond['user_id']
        total, result = AdviseService.advise_search_api(user_id=user_id, page=page, limit=limit)
        if total is False:
            return get_ret(result)
        else:
            return build_ret(success=True, total=total, data=result)
    else:
        return build_ret(success=True, msg="该接口还未开放！", code=404)


@route("/admin/advise/operation", api="后台反馈模块", methods=['GET', 'POST'])
def admin_advise():
    params = get_params()
    opr = params['opr']
    if opr == "add":
        # advise_id, content, user_id, message_type=1
        data = params['data']
        message_type = data['type']
        advise_id = data['advise_id']
        user_id = data['user_id']
        content = data['content']
        re_bool, result = AdviseService.advise_reply_api(advise_id=advise_id, content=content, user_id=user_id,
                                                         message_type=message_type)
        return get_ret(result)
    elif opr == "search":
        page = params['data']['page']
        limit = params['data']['limit']
        cond = params['data']['cond']
        login_name = cond['login_name'].strip()
        advise_type = cond['type']
        status = cond['status']
        if not advise_type:
            advise_type = None
        if not status:
            status = None
        total, result = AdviseService.advise_search_api(login_name=login_name, advise_type=advise_type,
                                                        status=status, page=page, limit=limit)
        if total is False:
            return get_ret(result)
        else:
            return build_ret(success=True, total=total, data=result)
    elif opr == "delete":
        advise_id = params['data']['id']
        re_bool, result = AdviseService.advise_del_api(advise_id=advise_id)
        return get_ret(result)
    else:
        return build_ret(success=True, msg="该接口还未开放！", code=404)