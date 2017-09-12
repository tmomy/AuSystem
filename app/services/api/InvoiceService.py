#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/9/9 10:51
"""
from ..InvoiceManageService import InvoiceOperate

invoice_entry_api = InvoiceOperate.invoice_entry
invoice_edit_api = InvoiceOperate.invoice_edit
invoice_search_api = InvoiceOperate.invoice_search
invoice_del_api = InvoiceOperate.invoice_del

invoice_admin_search_api = InvoiceOperate.admin_invoice_search

