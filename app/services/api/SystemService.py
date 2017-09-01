#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/9/1 16:06
"""
from ..SystemManageService import SystemOperate

service_init_api = SystemOperate.db_role_init
service_update_api = SystemOperate.db_role_update

rule_enable_api = SystemOperate.sys_enable_rule
