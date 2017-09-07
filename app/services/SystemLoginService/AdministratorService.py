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
from app.conf import msg
from .. import (engine, handler_commit, err_logging, field_update)

session = Session(engine)


@err_logging
def admin_login(account, password):
    administrator = session.query(Administrator).filter(Administrator.account == account).one_or_none()
    if not administrator:
        return False, msg.ERROR(1, "账号不存在！")
    if not (administrator.password == password):
        return False, msg.ERROR(1, "密码错误！")

    username = administrator.account
    user_id = administrator.id
    role_type = administrator.role_type
    token = en_token(username, user_id,role_type)
    handler_commit(session)
    return True, token


@err_logging
def admin_logout(token):
    redis_service.delete(token)
    return True, msg.SUCCESS
