#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/7/28 9:42
"""
from sqlalchemy.event import listens_for
from sqlalchemy.engine import Engine
from app.conf.config import pool_log_config, sqltime_log_config
from app.untils.log_builder import build_log
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sqltime_logger = build_log(sqltime_log_config)
pool_logger = build_log(pool_log_config)


@listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement,
                         parameters, context, executemany):
    conn.info.setdefault('query_start_time', time.time())
    # sqltime_logger.info("Start Query: {},Query Parameters: {}".format(str(statement), str(parameters)))


@listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement,
                         parameters, context, executemany):
    total = time.time() - conn.info['query_start_time']
    print total
    sqltime_logger.info("Start Query: {},Query Parameters: {},Query Complete!Total Time:{}".
                         format(str(statement), str(parameters), total))


@listens_for(Engine, "connect")
def my_on_connect(dbapi_connection, connection_record):
    # print("New DBAPI connection:", dbapi_connection)
    # print("Connection record:", connection_record)
    pass

