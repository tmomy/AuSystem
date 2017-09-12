#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/9/6 17:35
"""
from ..SystemLoginService.lib import en_token
from app.framework_api import redis_service
from app.Tables.AdministratorModel import Administrator
from sqlalchemy.orm import Session
from app.conf import msg,config
from .. import (engine, handler_commit, err_logging)

session = Session(engine)


@err_logging
def admin_login(account, password):
    if account == "root" and config.web['enable_admin']:
        username = "root"
        user_id = 0
        role_type = 1
        role_name = "root"
        token = en_token(username, user_id, role_type, role_name)
    else:
        administrator = session.query(Administrator).filter(Administrator.account == account).one_or_none()
        if not administrator:
            handler_commit(session)
            return False, msg.ERROR(1, "账号不存在！")
        if not (administrator.enable == 0):
            handler_commit(session)
            return False, msg.ERROR(1, "该账号已被禁用")
        if not (administrator.password == password):
            handler_commit(session)
            return False, msg.ERROR(1, "密码错误！")

        username = administrator.account
        user_id = administrator.id
        role_type = administrator.role_type
        role_name = administrator.role.name
        token = en_token(username, user_id, role_type, role_name)
        handler_commit(session)
    return True, token


@err_logging
def admin_logout(token):
    redis_service.delete(token)
    return True, msg.SUCCESS
