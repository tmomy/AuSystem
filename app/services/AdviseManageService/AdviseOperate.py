#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/9/8 9:40
"""
import json
from sqlalchemy.orm import Session
from app.Tables.AdviseTable import Advise
from app.Tables.MessageTable import Message
from app.Tables.userModel import User
from app.conf import msg, config
from app.untils.context_get import get_user_info
from sqlalchemy import and_, or_
from .. import engine, handler_commit, err_logging

session = Session(engine)


# __init__(self, advise_type, tel, desc, pics, user_id):
@err_logging
def advise_entry(advise_type, tel, desc, pics):
    user_info = get_user_info()
    if not isinstance(pics, list):
        return False, msg.ERROR(1, "pics输入类型错误!")
    entry_advise = Advise(advise_type=advise_type, tel=tel, desc=desc, pics=pics, user_id=user_info.get("user_id"))
    session.add(entry_advise)
    return handler_commit(session)


@err_logging
def advise_search(login_name=None, user_id=None, advise_type=None, status=None, page=1, limit=10):
    offset = (page - 1) * limit
    data = []
    if login_name:
        search_user = session.query(User).filter(User.login_name == login_name).one_or_none()
        if search_user:
            user_id = search_user.user_id
        else:
            user_id = None
        search_advise = session.query(Advise).filter(Advise.user_id == user_id)\
            .order_by(Advise.create_time.desc())
    elif user_id:
        search_advise = session.query(Advise).filter(Advise.user_id == user_id)\
            .order_by(Advise.create_time.desc())
    elif advise_type and status:
        search_advise = session.query(Advise).filter(and_(Advise.status == status, Advise.type == advise_type))\
            .order_by(Advise.create_time.desc())
    elif not advise_type and not status:
        search_advise = session.query(Advise).order_by(Advise.create_time.desc())
    else:
        search_advise = session.query(Advise).filter(or_(Advise.status == status, Advise.type == advise_type))\
            .order_by(Advise.create_time.desc())

    total = search_advise.count()
    for adv in search_advise.offset(offset).limit(limit):
        data.append(adv.to_json())
    handler_commit(session)
    return total, data


@err_logging
def advise_del(advise_id):
    del_result = session.query(Advise).filter(Advise.id == advise_id).delete(synchronize_session=False)
    handler_commit(session)
    if del_result == 1:
        return True, msg.ERROR(0, "删除成功！")
    else:
        return False, msg.ERROR(1, "记录不存在！")


# waiter_id, message_type, detail, user_id
@err_logging
def advise_reply(advise_id, content, user_id, message_type=1):
    user_info = get_user_info()
    waiter_id = user_info["user_id"]
    message = Message(waiter_id=waiter_id, message_type=message_type, detail=content,
                      user_id=user_id, reply_id=advise_id)
    session.query(Advise).filter(Advise.id == advise_id).update({Advise.status: 0}, synchronize_session=False)
    session.add(message)
    return handler_commit(session)



