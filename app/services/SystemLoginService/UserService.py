#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/9/6 17:34
"""
from ..SystemLoginService.lib import en_token
from app.framework_api import redis_service
from app.Tables.userModel import User
from sqlalchemy.orm import Session
from app.conf import msg
import json, random
from app.untils.sms import send_sms_dy as send
from app.conf.config import web, red_pre,R_SMS
from .. import (engine, handler_commit, err_logging, field_update)

session = Session(engine)


@err_logging
def user_login(account, password):
    user = session.query(User).filter(User.login_name == account).one_or_none()
    if not user:
        return False, msg.ERROR(1, "账号不存在！")
    if not (user.login_pass == password):
        return False, msg.ERROR(1, "密码错误！")

    username = user.login_name
    user_id = user.user_id
    role_type = user.role_type
    role_name = user.role.name
    token = en_token(username=username, user_id=user_id,role_type=role_type, role_name=role_name)
    handler_commit(session)
    return True, token


@err_logging
def sms_send(account):
    return send_sms(account)


@err_logging
def sms_login(account, code):
    user = session.query(User).filter(User.login_name == account).one_or_none()
    if not user:
        return False, msg.ERROR(1, "账号不存在！")
    if get_code(account) != code:
        return False, msg.ERROR(1, "验证码错误！")
    username = user.login_name
    user_id = user.user_id
    role_type = user.role_type
    role_name = user.role.name
    token = en_token(username, user_id, role_type, role_name)
    handler_commit(session)
    return True, token


@err_logging
def sms_login_send(account):
    user = session.query(User).filter(User.login_name == account).one_or_none()
    if not user:
        return False, msg.ERROR(1, "账号不存在！")
    handler_commit(session)
    return send_sms(account)


@err_logging
def user_logout(token):
    redis_service.delete(token)
    return True, msg.SUCCESS


def set_code(sms_code, mobile):
    """
    存储短信验证码，生命周期为60s
    :param sms_code: type(string) 短信验证码
    :param mobile:  type(string) 手机号
    :return: 
    """
    redis_service.setex(mobile+red_pre['code'], R_SMS['redis_timeout'], sms_code)
    pass


def get_code(mobile):
    """
    从redis取出短信验证码
    :param mobile: type(string) 手机号
    :return: 
    """
    return redis_service.get(mobile + red_pre['code'])


def send_sms(mobile):
    """
    处理短语验证码发送的逻辑函数
    :param mobile: type(string) 手机号
    :return: 
    """
    if get_code(mobile+red_pre['code']):
        return msg.A_MAX_REQUEST
    __param = {}
    __sms_code = generate_code()
    __param[R_SMS['template_string']] = __sms_code
    param = json.dumps(__param)
    sms_response = send(mobile, param)
    if sms_response:
        set_code(__sms_code, mobile)
        return True, msg.SUCCESS
    else:
        return False, msg.A_SMS_ERR


def generate_code():
    """
    生成6位短信验证码
    :return: 
    """
    random_seeds = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    str_slice = random.sample(random_seeds, 6)
    sms_code = ''.join(str_slice)
    return sms_code
