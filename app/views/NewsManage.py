#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2017/9/8 16:29
"""
from app.untils import get_params
from app.framework_api import route, build_ret
from app.services.api import NewsServices
from app.untils.context_get import get_user_info


# admin新闻类型操作
# 增加
@route("/admin/news/type/add", api="news", methods=['GET', 'POST'])
def news_type_add():
    params = get_params()
    result = NewsServices.service_news_type_add(params)
    return build_ret(success=result)


# 编辑
@route("/admin/news/type/modify", api="news", methods=['GET', 'POST'])
def news_type_modify():
    params = get_params()
    result = NewsServices.service_news_type_modify(params)
    return build_ret(success=result)


# 查询
@route("/admin/news/type/list", api="news", methods=['GET', 'POST'])
def news_type_list():
    # params = get_params()
    result, total = NewsServices.service_news_type_list()
    return build_ret(success=True, data=result, total=total)

# 删除
@route("/admin/news/type/del", api="news", methods=['GET', 'POST'])
def news_type_del():
    params = get_params()
    result = NewsServices.service_news_type_del(params['id'])
    return build_ret(success=result)


# 新闻模块增加
# 增加
@route("/admin/news/add", api="news", methods=['GET', 'POST'])
def news_add():
    params = get_params()
    result = NewsServices.service_news_add(params)
    return build_ret(success=result)


# 编辑
@route("/admin/news/modify", api="news", methods=['GET', 'POST'])
def news_modify():
    params = get_params()
    result = NewsServices.service_news_modify(params)
    return build_ret(success=result)


# 查询
@route("/admin/news/list", api="news", methods=['GET', 'POST'])
def news_list():
    params = get_params()
    result, total = NewsServices.service_news_list(params)
    return build_ret(success=True, data=result, total=total)


# 删除
@route("/admin/news/del", api="news", methods=['GET', 'POST'])
def news_del():
    params = get_params()
    result = NewsServices.service_news_del(params['id'])
    return build_ret(success=result)


# 详情
@route("/admin/news/detail", api="news", methods=['GET', 'POST'])
def news_del():
    params = get_params()
    result = NewsServices.service_news_detail(params['id'])
    return build_ret(success=result, data=result)


# app端新闻模块接口
# 新闻类型查询
@route("/app/news/type/list", api="news", methods=['GET', 'POST'])
def app_news_type_list():
    # params = get_params()
    result, total = NewsServices.service_news_type_list()
    return build_ret(success=True, data=result, total=total)


# 新闻查询
@route("/app/news/list", api="news", methods=['GET', 'POST'])
def app_news_list():
    params = get_params()
    result, total = NewsServices.service_news_list(params)
    return build_ret(success=True, data=result, total=total)


# 新闻详情
@route("/app/news/detail", api="news", methods=['GET', 'POST'])
def app_news_del():
    params = get_params()
    result = NewsServices.service_news_detail(params['id'])
    return build_ret(success=result, data=result)