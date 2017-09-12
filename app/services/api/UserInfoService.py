#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/9/11 16:13
"""
from ..UserInfoService import UserInfoOperate


# 修改绑定手机号
account_send_api = UserInfoOperate.send_code
account_valid_api = UserInfoOperate.valid_code

account_info_api = UserInfoOperate.user_info_search
account_edit_api = UserInfoOperate.account_info_edit
