#!/usr/bin/env python
# encoding: utf-8
"""
@author: XX
@time: 2017/9/5 10:55
"""
from app.untils import get_params
from app.framework_api import route, build_ret, get_ret
from app.services.api import ProductService


@route("/product/attribute", api="product/attribute", methods=['GET', 'POST'])
def attribute():
    params = get_params()
    opr = params['opr']
    if opr == "add":
        resp, msg = ProductService.service_attribute_add(params=params["data"])
        return get_ret(error=msg)
    elif opr == "search":
        result = ProductService.service_attribute_search(params=params["data"])
        return build_ret(success=True, data=result)
    elif opr == "delete":
        resp, msg = ProductService.service_attribute_delete_attr(params=params["data"])
        return get_ret(error=msg)


@route("/product/attribute/value", api="product/attribute/value", methods=['GET', 'POST'])
def attr_value():
    params = get_params()
    opr = params['opr']
    if opr == "delete":
        resp, msg = ProductService.service_attribute_delete_value(params=params["data"])
        return get_ret(error=msg)