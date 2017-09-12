#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/9/7 10:04
"""
from flask import make_response, request
from app.untils import get_params
from app.framework_api import route, build_ret, get_ret
from app.services.api import SystemLoginService


@route("/admin/login", type=True, api="后台管理系统登录", methods=['GET', 'POST'])
def admin_login():
    params = get_params()
    opr = params['opr']
    if opr == "add":
        data = params['data']
        account = data['account']
        password = data['password']
        re_bool, result = SystemLoginService.admin_login_api(account=account, password=password)
        if re_bool:
            resp = build_ret(success=True, msg="登录成功！")
            response = make_response(resp)
            response.headers['authorization'] = result
            return response
        else:
            return get_ret(result)
    else:
        return build_ret(success=True, msg="该接口还未开放！", code=404)


@route("/admin/logout", api="后台管理系统注销", methods=['GET', 'POST'])
def admin_logout():
    params = get_params()
    opr = params['opr']
    if opr == "add":
        token = request.headers.get('authorization')
        re_bool, result = SystemLoginService.admin_logout_api(token)
        if re_bool:
            return get_ret(result)
        else:
            return get_ret(result)
    else:
        return build_ret(success=True, msg="该接口还未开放！", code=404)


@route("/account/login", type=True, api="会员登录", methods=['GET', 'POST'])
def account_login():
    params = get_params()
    opr = params['opr']
    if opr == "add":
        data = params['data']
        account = data['account']
        password = data['password']
        re_bool, result = SystemLoginService.user_login_api(account=account, password=password)
        if re_bool:
            resp = build_ret(success=True, msg="登录成功！")
            response = make_response(resp)
            response.headers['authorization'] = result
            return response
        else:
            return get_ret(result)
    else:
        return build_ret(success=True, msg="该接口还未开放！", code=404)


@route("/account/sms/login", type=True,  api="短信登录", methods=['GET', 'POST'])
def account_login():
    params = get_params()
    opr = params['opr']
    if opr == "add":
        data = params['data']
        account = data['account']
        code = data['code']
        re_bool, result = SystemLoginService.sms_login_api(account=account, code=code)
        if re_bool:
            resp = build_ret(success=True, msg="登录成功！")
            response = make_response(resp)
            response.headers['authorization'] = result
            return response
        else:
            return get_ret(result)
    else:
        return build_ret(success=True, msg="该接口还未开放！", code=404)


@route("/account/sms", type=True, api="短信登录-短信验证码", methods=['GET', 'POST'])
def account_login():
    params = get_params()
    opr = params['opr']
    if opr == "add":
        data = params['data']
        account = data['account']
        re_bool, result = SystemLoginService.sms_send_api(account=account)
        if re_bool:
            resp = build_ret(success=True, msg="短信已发送！")
            return resp
        else:
            return get_ret(result)
    else:
        return build_ret(success=True, msg="该接口还未开放！", code=404)


@route("/account/logout", api="会员注销", methods=['GET', 'POST'])
def account_logout():
    params = get_params()
    opr = params['opr']
    if opr == "add":
        token = request.headers.get('authorization')
        re_bool, result = SystemLoginService.user_logout_api(token)
        if re_bool:
            return get_ret(result)
        else:
            return get_ret(result)
    else:
        return build_ret(success=True, msg="该接口还未开放！", code=404)