#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/9/11 14:23
"""
from sqlalchemy.orm import Session
from flask import request
from app.Tables.userModel import User
from app.conf import msg
from app.conf.config import red_pre
from app.untils import get_user_info
from ..api.SystemLoginService import sys_get_code_api, sys_send_sms_api, user_logout_api
from .. import engine, handler_commit, err_logging, field_update
from app.framework_api import redis_service

session = Session(engine)


@err_logging
def user_info_search():
    user_info = get_user_info()
    user_id = user_info['user_id']
    search_user = session.query(User).filter(User.user_id == user_id).one_or_none()
    if not search_user:
        return False, msg.ERROR(1,"记录不存在！")
    detail = search_user.to_json()
    re_info = {
        'user_id': detail['user_id'],
        'avatar': detail['avatar'],
        'nick_name': detail['nick_name'],
        'name': detail['name'],
        'tel': detail['tel'],
        'sex': detail['sex'],
        'birthday': detail['birthday']
    }
    return True, re_info


@err_logging
def valid_code( code, mobile=None, valid_type="original"):
    if valid_type not in ['original','update']:
        return False, msg.ERROR(1, "输入错误！")
    user_info = get_user_info()
    user_id = user_info['user_id']
    search_user = session.query(User).filter(User.user_id == user_id).one_or_none()
    or_mobile = search_user.login_name
    lock_keys = red_pre['sms_lock_pix'] + "original" + or_mobile
    valid_lock = redis_service.lpop(lock_keys)
    if valid_type == "original":
        valid_lock = True
        mobile = or_mobile
    if not valid_lock:
        return False, msg.ERROR(1, "无效验证码！")
    valid_num = sys_get_code_api(mobile)
    if not valid_num:
        return False, msg.ERROR(1, "验证码失效！")
    if valid_num != code:
        return False, msg.ERROR(1, "验证码错误！")
    if valid_type == "update":
        update_result = login_name_modify(mobile)
        if update_result[0]:
            token = request.headers.get('authorization')
            return user_logout_api(token)
        return update_result
    else:
        redis_service.lpush(lock_keys, or_mobile)
        return True, msg.SUCCESS


@err_logging
def send_code(mobile=None, valid_type="original"):
    user_info = get_user_info()
    user_id = user_info['user_id']
    search_user = session.query(User).filter(User.user_id == user_id).one_or_none()
    or_mobile = search_user.login_name
    if valid_type == "original":
        send_result = sys_send_sms_api(or_mobile)
        if send_result[0]:
            redis_service.lpush(or_mobile+valid_type, or_mobile)
        return send_result
    elif valid_type == "update":
        step_lock = redis_service.lpop(or_mobile+"original")
        if not step_lock:
            return False, msg.ERROR(1, "执行操作异常！")
        exist_user = session.query(User).filter(User.login_name == mobile).one_or_none()
        if exist_user:
            return False, msg.ERROR(1, "新手机号已存在记录！")
        send_result = sys_send_sms_api(mobile)
        if send_result[0]:
            redis_service.lpush(mobile + valid_type, mobile)
        return send_result


@err_logging
def login_name_modify(mobile):
    user_info = get_user_info()
    user_id = user_info['user_id']
    search_user = session.query(User).filter(User.user_id == user_id).one_or_none()
    if not search_user:
        return False, msg.ERROR(1,"记录不存在！")
    search_user.login_name = mobile
    session.flush()
    return handler_commit(session)


@err_logging
def account_info_edit(field, value):
    if field not in ["avatar", "nick_name", "name", "tel", "birthday"]:
        return False, msg.ERROR(1, "输入异常！")
    user_info = get_user_info()
    user_id = user_info['user_id']
    search_account = session.query(User).filter(User.user_id == user_id).one_or_none()
    modify_result = field_update(search_account, field, value)
    session.flush()
    return handler_commit(session)
