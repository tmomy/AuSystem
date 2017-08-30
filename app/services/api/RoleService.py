#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/8/28 15:24
"""
from ..RoleManageService import operate
service_init_api = operate.db_role_init
service_update_api = operate.db_role_update
role_create_api = operate.db_role_add
role_edit_api = operate.db_role_modify
role_del_api = operate.db_role_del
role_search_api = operate.db_role_search

