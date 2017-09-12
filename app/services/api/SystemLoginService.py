#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/9/7 10:01
"""
from ..SystemLoginService import AdministratorService, UserService

# administrator
admin_login_api = AdministratorService.admin_login
admin_logout_api = AdministratorService.admin_logout

# user
user_login_api = UserService.user_login
user_logout_api = UserService.user_logout
sms_send_api = UserService.sms_login_send
sms_login_api = UserService.sms_login

# basic service
sys_send_sms_api = UserService.send_sms
sys_get_code_api = UserService.get_code

