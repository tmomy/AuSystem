#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/9/4 17:54
"""
from sqlalchemy.orm import Session
from app.Tables.AdministratorModel import Administrator
from app.Tables.RoleManage import Role
from app.conf import msg
from .. import engine, handler_commit, err_logging, field_update

session = Session(engine)


# account, password, role_type=2, enable=0
@err_logging
def admin_add(account, password, role_type, enable):
    role = session.query(Role).filter(Role.role_id == role_type).one_or_none()
    if role is None:
        return False, msg.ERROR(1, "角色类型不存在！")
    entry_admin = Administrator(account, password, role_type, enable)
    session.add(entry_admin)
    return handler_commit(session)


@err_logging
def admin_edit(admin_id, edit_info):
    # role = session.query(Role).filter(Role.role_id == edit_info['role_type']).one_or_none()
    # if role is None:
    #     return False, msg.ERROR(1, "角色类型不存在！")
    search_admin = session.query(Administrator).filter(Administrator.id == admin_id).one_or_none()
    if not search_admin:
        return False, msg.ERROR(1, "用户不存在！")
    for field, value in edit_info.items():
        result = field_update(search_admin, field, value)
        if not result:
            return False, msg.ERROR(1, "{}字段不存在".format(field))
    session.flush()
    return handler_commit(session)


@err_logging
def admin_search(page=1, limit=10):
    offset = (page - 1) * limit
    data = []
    search_admin = session.query(Administrator)
    total = search_admin.count()
    for admin in search_admin.offset(offset).limit(limit):
        print admin.to_json()
        data.append(admin.to_json())
    handler_commit(session)
    print data
    return total, data


@err_logging
def admin_del(admin_id):
    search_account = session.query(Administrator).filter(Administrator.id == admin_id).delete(synchronize_session=False)
    handler_commit(session)
    if search_account == 1:
        return True, msg.ERROR(0, "删除成功！")
    else:
        return False, msg.ERROR(1, "用户不存在！")