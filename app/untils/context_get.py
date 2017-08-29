#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/8/28 14:32
"""
from flask import request


def get_params():
    params = getattr(request,"params")
    return params


def get_rule_set():
    rule_set = getattr(request, "rule_set")
    if rule_set is None:
        rule_set = []
    return rule_set

