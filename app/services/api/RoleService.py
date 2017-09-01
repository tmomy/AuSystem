#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/8/28 15:24
"""
from ..RoleManageService import operate

role_create_api = operate.db_role_add
role_edit_api = operate.db_role_modify
role_del_api = operate.db_role_del
role_search_api = operate.db_role_search

role_rule_del = operate.db_role_rule_delete

relationship_add_api = operate.db_relationship_add
relationship_del_api = operate.db_relationship_del
relationship_search_api = operate.db_relationship_search
relationship_edit_api = operate.db_relationship_edit

route_search_api = operate.db_route_search
route_edit_api = operate.db_route_edit

