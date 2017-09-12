#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/9/9 10:12
"""
from sqlalchemy.orm import Session
from app.Tables.InvoiceTable import Invoice
from app.Tables.userModel import User
from app.conf import msg, config
from app.untils.context_get import get_user_info
from sqlalchemy import and_, or_
from .. import engine, handler_commit, err_logging, field_update

session = Session(engine)


# invoice_type, invoice_name, tel, person_address, user_id, email="", company_num=""
@err_logging
def invoice_entry(invoice_type, invoice_name, tel, person_address, email=None, company_num=None):
    user_info = get_user_info()
    user_id = user_info['user_id']
    if email and company_num:
        return False, msg.ERROR(1, "输入异常！")
    elif invoice_type in [0, 1] and invoice_type and company_num:  # invoice_type 0/1, 0:个人; 1:公司
        entry_invoice = Invoice(invoice_type=invoice_type, invoice_name=invoice_name, tel=tel,
                                person_address=person_address, user_id=user_id, company_num=company_num)
    elif invoice_type in [0, 1] and email:
        entry_invoice = Invoice(invoice_type=invoice_type, invoice_name=invoice_name, tel=tel,
                                person_address=person_address, user_id=user_id, email=email)
    else:
        return False, msg.ERROR(1, "输入异常！")
    session.add(entry_invoice)
    return handler_commit(session)


@err_logging
def invoice_edit(invoice_id, edit_info):
    user_info = get_user_info()
    user_id = user_info['user_id']
    search_invoice = session.query(Invoice).filter(and_(Invoice.id == invoice_id, Invoice.user_id == user_id))\
        .one_or_none()
    if not search_invoice:
        return False, msg.ERROR(1, "该记录不存在！")
    for field, value in edit_info.items():
        result = field_update(search_invoice, field, value)
        if not result:
            return False, msg.ERROR(1, "{}字段不存在".format(field))
    session.flush()
    return handler_commit(session)


@err_logging
def invoice_search(invoice_id, page=1, limit=10):
    offset = (page - 1) * limit
    data = []
    total = 0
    user_info = get_user_info()
    user_id = user_info['user_id']
    if invoice_id:
        search_invoice = session.query(Invoice).filter(and_(Invoice.user_id == user_id, Invoice.id == invoice_id))\
            .one_or_none()
        if search_invoice:
            data.append(search_invoice.to_json())
            total = 1
    else:
        search_invoice = session.query(Invoice).filter(Invoice.user_id == user_id).order_by(Invoice.create_time.desc())
        total = search_invoice.count()
        for adv in search_invoice.offset(offset).limit(limit):
            data.append(adv.to_json())
    handler_commit(session)
    return total, data


@err_logging
def admin_invoice_search(login_name=None, invoice_type=None, company_num=None,  page=1, limit=10):
    offset = (page - 1) * limit
    data = []
    user_id = None
    if login_name:
        user = session.query(User).filter(User.login_name == login_name).one_or_none()
        if user:
            user_id = user.user_id
    if company_num:
        search_invoice = session.query(Invoice).filter(Invoice.company_num == company_num)\
            .order_by(Invoice.create_time.desc())
    elif user_id and str(invoice_type):
        search_invoice = session.query(Invoice).filter(and_(Invoice.user_id == user_id, Invoice.type == invoice_type))\
            .order_by(Invoice.create_time.desc())
    elif user_id:
        search_invoice = session.query(Invoice).filter(Invoice.user_id == user_id).order_by(Invoice.create_time.desc())
    elif str(invoice_type):
        search_invoice = session.query(Invoice).filter(Invoice.type == invoice_type)\
            .order_by(Invoice.create_time.desc())
    else:
        search_invoice = session.query(Invoice).order_by(Invoice.create_time.desc())
    total = search_invoice.count()
    for inv in search_invoice.offset(offset).limit(limit):
        data.append(inv.to_json())
    handler_commit(session)
    return total, data


@err_logging
def invoice_del(invoice_id):
    user_info = get_user_info()
    user_id = user_info['user_id']
    del_result = session.query(Invoice).filter(and_(Invoice.user_id == user_id, Invoice.id == invoice_id))\
        .delete(synchronize_session=False)
    handler_commit(session)
    if del_result == 1:
        return True, msg.ERROR(0, "删除成功！")
    else:
        return False, msg.ERROR(1, "记录不存在！")