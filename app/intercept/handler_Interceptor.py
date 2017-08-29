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
from app.conf.config import log


logging = build_log(log_config=log)


@app.before_request
def context_handler():
    setattr(request, 'rule_set', rules)
    pass


@app.after_request
def response_handler(response):
    logging.info("response is [{}]".format(response.data))
    return response

