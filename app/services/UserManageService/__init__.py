#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/8/25 17:33
"""
from sqlalchemy.ext.declarative import declarative_base
from app.mysql_db import db_pool
ModelBase = declarative_base()
engine = db_pool

