# encoding: utf-8

"""
@version: 1.0
@author: dawning
@contact: dawning7670@gmail.com
@time: 2017/3/29 11:02
"""
import traceback
import threading
from app.conf import web
from framework.flask import app
from framework.exception.validator import JSONValidateError
from framework.utils import build_ret
from framework.utils import logging

err_id = threading._get_ident()


# 异常统一处理
@app.errorhandler(JSONValidateError)
def json_validate_error(e):
    response = build_ret(False, msg=e.message, code=err_id)
    logging.error("err_id:{}{}".format(err_id,traceback.format_exc()))
    return response


@app.errorhandler(Exception)
def internal_error(e):
    if web['debug']:
        response = build_ret(False, msg=e.message, code=err_id)
    else:
        response = build_ret(False, msg="意外错误", code=err_id)
    logging.error("err_id:{}{}".format(err_id,traceback.format_exc()))
    return response


# 处理404页面
@app.errorhandler(404)
def not_found(e):
    response = build_ret(False, msg="页面不存在")
    return response


# 处理400页面
@app.errorhandler(400)
def bad_request(e):
    print e
    response = build_ret(False, msg="请求错误", code=err_id)
    logging.error("err_id:{}{}".format(err_id,traceback.format_exc()))
    return response
