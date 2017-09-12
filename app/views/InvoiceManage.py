#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/9/9 11:01
"""
from app.untils import get_params
from app.framework_api import route, build_ret, get_ret
from app.services.api import InvoiceService


@route("/invoice/operation", api="发票模块", methods=['GET', 'POST'])
def advise():
    params = get_params()
    opr = params['opr']
    if opr == "add":
        # invoice_type, invoice_name, tel, person_address,email="", company_num=""
        data = params['data']
        invoice_type = data['type']
        invoice_name = data['invoice_name']
        tel = data['tel']
        person_address = data['person_address']
        email = data.get('email')
        company_num = data.get('company_num')
        re_bool, result = InvoiceService.invoice_entry_api(invoice_type=invoice_type, invoice_name=invoice_name,
                                                           tel=tel, person_address=person_address, email=email,
                                                           company_num=company_num)
        return get_ret(result)
    # invoice_id
    elif opr == "search":
        page = params['data']['page']
        limit = params['data']['limit']
        cond = params['data']['cond']
        invoice_id = cond['id']
        total, result = InvoiceService.invoice_search_api(invoice_id=invoice_id, page=page, limit=limit)
        if total is False:
            return get_ret(result)
        else:
            return build_ret(success=True, total=total, data=result)
    elif opr == "delete":
        invoice_id = params['data']['id']
        re_bool, result = InvoiceService.invoice_del_api(invoice_id=invoice_id)
        return get_ret(result)
    elif opr == "modify":
        data = params['data']
        edit_info = dict()
        edit_info['invoice_name'] = data['invoice_name']
        edit_info['tel'] = data['tel']
        edit_info['person_address'] = data['person_address']
        edit_info['company_num'] = data.get('company_num', "")
        edit_info['email'] = data.get('email', "")
        invoice_id = data.pop('id')
        if edit_info['company_num'] and edit_info['email']:
            return build_ret(success=False, msg="输入异常！")
        re_bool, result = InvoiceService.invoice_edit_api(invoice_id=invoice_id, edit_info=edit_info)
        return get_ret(result)
    else:
        return build_ret(success=True, msg="该接口还未开放！", code=404)


@route("/admin/invoice/operation", api="后台发票查询", methods=['GET', 'POST'])
def advise():
    params = get_params()
    opr = params['opr']
    # invoice_id
    if opr == "search":
        page = params['data']['page']
        limit = params['data']['limit']
        cond = params['data']['cond']
        login_name = cond['login_name']
        invoice_type = cond['type']
        company_num = cond['company_num']
        total, result = InvoiceService.invoice_admin_search_api(login_name=login_name, invoice_type=invoice_type,
                                                                company_num=company_num, page=page, limit=limit)
        if total is False:
            return get_ret(result)
        else:
            return build_ret(success=True, total=total, data=result)
    else:
        return build_ret(success=True, msg="该接口还未开放！", code=404)
