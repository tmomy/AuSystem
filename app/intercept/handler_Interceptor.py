#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/8/25 9:52
"""
from framework.flask import app
from framework.decorators import rules
from flask import request,make_response, g
from app.untils.log_builder import build_log
from app.conf.config import log, web
from app.framework_api import redis_service
import threading

_ident = threading._get_ident()


logging = build_log(log_config=log)


@app.before_request
def context_handler():
    redis_key = web['rule_redis_pix'] + "1"
    if request.path == "/api/tiptop/v1/admin/system/role":
        return make_response("12344",404)
    # rule_dict = redis_service.get(redis_key)
    setattr(request, 'rule_set', rules)
    pass


@app.after_request
def response_handler(response):
    redis_key = web['rule_redis_pix'] + "1"
    print redis_key
    rule_dict = redis_service.get(redis_key)
    print rule_dict
    logging.info("response is [{}]".format(response.data))
    return response

