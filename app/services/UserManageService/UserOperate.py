#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/8/26 15:18
"""

from sqlalchemy.orm import Session
from app.Tables.userModel import User
from app.Tables.AccountAddress import Address
from app.conf import msg
from .. import engine, handler_commit, err_logging, field_update

session = Session(engine)


# 手机号/加入时间2017.9.1/会员期限365/年费
@err_logging
def account_entry(account_info):
    nick_pix = "user"
    entry_account = User()
    role_type = 3
    account_info['nick_name'] = nick_pix + account_info['login_name']
    account_info['tel'] = account_info['login_name']
    account_info['role_type'] = role_type
    for field , value in account_info.items():
        if field in ['rest_day', 'user_integral']:
            field_update(entry_account, field, value)
        else:
            field_update(entry_account, field, value)
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
def account_search(sort, login_name=None, enable=None, page=1, limit=10):
    offset = (page - 1) * limit
    data = []
    total = 0

    if login_name:
        search_account = session.query(User).filter(User.login_name == login_name).one_or_none()
        if search_account:
            total = 1
            data.append(search_account.to_json())
    elif enable is not None:
        search_account = session.query(User).filter(User.enable == int(enable)).order_by(*_account_sort_handler(sort))
        total = search_account.count()
        for account in search_account.offset(offset).limit(limit):
            data.append(account.to_json())
    else:
        search_account = session.query(User).order_by(*_account_sort_handler(sort))
        total = search_account.count()
        for account in search_account.offset(offset).limit(limit):
            data.append(account.to_json())
    handler_commit(session)
    return total, data


@err_logging
def account_del(user_id):
    search_account = session.query(User).filter(User.user_id == user_id).delete(synchronize_session=False)
    handler_commit(session)
    if search_account == 1:
        return True, msg.ERROR(0, "删除成功！")
    else:
        return False, msg.ERROR(1, "用户不存在！")


@err_logging
def account_address_add(address_info):
    user_id = address_info.pop('user_id')
    user_info = session.query(User).filter(User.user_id==user_id).one_or_none()
    if not user_info:
        return False, msg.ERROR(1, "用户不存在！")
    entry_address = Address(user_info)
    for field, value in address_info.items():
        result = field_update(entry_address, field, value)
        if not result:
            return False, msg.ERROR(1, "{}字段不存在".format(field))
    session.add(entry_address)
    return handler_commit(session)


@err_logging
def account_address_search(login_name, page=1, limit=10):
    offset = (page - 1) * limit
    data = []
    if login_name:
        search_address = session.query(Address).filter(Address.login_name == login_name)
        total = search_address.count()
    else:
        search_address = session.query(Address)
        total = search_address.count()
    for adr in search_address.offset(offset).limit(limit):
        data.append(adr.to_json())
    handler_commit(session)
    return total, data


def _account_sort_handler(sort):
    if not sort:
        sort = {
          "register_time": 0
        }
    sort_mapping = {
          "rest_day": User.rest_day,
          "-rest_day": User.rest_day.desc(),
          "enable": User.enable,
          "-enable": User.enable.desc(),
          "user_integral": User.user_integral,
          "-user_integral": User.user_integral.desc(),
          "register_time": User.register_time,
          "-register_time": User.register_time.desc()
          }
    sort_list = []
    for key, value in sort.items():
        if not int(value):
            key = "-" + key
        sort_list.append(sort_mapping[key])
    return tuple(sort_list)




