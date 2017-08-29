#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/7/27 17:56
"""
from db_pool import engine
db_pool = engine()



__all__ = (
    'db_pool',
)

