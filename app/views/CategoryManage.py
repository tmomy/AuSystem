#!/usr/bin/env python
# encoding: utf-8
"""
@author: XX
@time: 2017/9/5 10:54
"""
from app.untils import get_params
from app.framework_api import route, build_ret, get_ret
from app.services.api import ProductService


@route("/product/category", api="category", methods=['GET', 'POST'])
def category():
    params = get_params()
    opr = params['opr']
    if opr == "add":
        resp, msg = ProductService.service_category_add(params=params['data'])
        return get_ret(error=msg)
    elif opr == "search":
        if params['data']['format'] == "tree":
            result = ProductService.service_category_tree()
            return build_ret(success=True, data=result)
        elif params['data']['format'] == "table":
            result, total = ProductService.service_category_table(params=params['data'])
            return build_ret(success=True, data=result, total=total)
    elif opr == "delete":
        resp, msg = ProductService.service_category_delete(category_id=params["data"]["category_id"])
        return get_ret(error=msg)
    elif opr == "modify":
        resp, msg = ProductService.service_category_edit(params=params['data'])
        return get_ret(error=msg)


@route("/product/category/child", api="category", methods=['GET', 'POST'])
def category():
    params = get_params()
    opr = params['opr']
    if opr == "search":
        result = ProductService.service_category_getOne(params=params['data'])
        return build_ret(success=True, data=result)
