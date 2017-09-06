#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/9/4 15:24
"""
from ..UserManageService import UserOperate, AdminOperate

admin_account_entry_api = UserOperate.account_entry
admin_account_edit_api = UserOperate.account_edit
admin_account_search_api = UserOperate.account_search
admin_account_del_api = UserOperate.account_del

admin_administrator_add_api = AdminOperate.admin_add
admin_administrator_edit_api = AdminOperate.admin_edit
admin_administrator_del_api = AdminOperate.admin_del
admin_administrator_search_api = AdminOperate.admin_search

address_add_api = UserOperate.account_address_add
address_search_api = UserOperate.account_address_search

