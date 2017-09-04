#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/8/26 15:18
"""

from sqlalchemy.orm import Session

from app.Tables.userModel import User
from app.conf import msg
from .. import engine, handler_commit, err_logging, field_update

session = Session(engine)


# 手机号/加入时间2017.9.1/会员期限365/年费
@err_logging
def account_entry(account, effective_time, rest_day, user_integral):
    int_rest_day = int(rest_day)
    int_user_integral = int(user_integral)
    role_type = 3
    entry_account = User(login_name=account, effective_time=effective_time,
                         role_type=role_type, rest_day=int_rest_day, user_integral=int_user_integral)

    session.add(entry_account)
    result = handler_commit(session)
    if result[0]:
        return result
    else:
        return False, msg.ERROR(1, "账号已存在！")


@err_logging
def account_edit(user_id, account_info):
    search_account = session.query(User).filter(User.user_id == user_id).one_or_none()
    if not search_account:
        return False, msg.ERROR(1, "用户不存在！")
    for field, value in account_info.items():
        edit_result = field_update(search_account, field, value)
        if not edit_result:
            return False, msg.ERROR(1, "输入不合法字段{}".format(field))
    session.flush()
    return handler_commit(session)


@err_logging
def account_search(user_id=None, page=1, limit=10):
    offset = (page - 1) * limit
    data = []
    total = 0
    if user_id:
        search_account = session.query(User).order_by(User.user_id)
    pass






