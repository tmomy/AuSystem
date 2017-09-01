#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2017/8/31 10:10
"""
import time, random
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.Tables.taskModel import Task
from app.conf import msg
from app.untils import get_rule_set
from .. import engine, handler_commit

session = Session(engine)


# 新增任务

def task_add():
    # 应该获取会员登录手机号
    data = {
        'user_id': '',
        'tasks': [
            {'task_num': 2, 'task_do_time': '2017-09-01'},
            {'task_num': 0, 'task_do_time': '2017-09-02'},
            {'task_num': 3, 'task_do_time': '2017-09-03'}
        ]
    }
    for task in data['tasks']:
        sql_result = session.query(Task).filter(
            and_(
                # Task.user_id == data['user_id'],
                Task.task_do_time == task['task_do_time'],
            ))
        # 该用户是否存在记录 存在则覆盖 不存在新增
        # 并且对将task_num=1的进行处理 有则删掉 无则不处理
        if sql_result.count() is not 0:
            if task['task_num'] is 1:
                session.delete(sql_result.one())
            else:
                sql_result.one().task_num = task['task_num']
        else:
            if task['task_num'] is not 1:
                session.add(Task(task_num=task['task_num'], task_do_time=task['task_do_time']))

    result = handler_commit(session)
    return result


# 查询任务

def task_list():
    cond = {
        'user_id': '',
        'start_time': '2017-09-01',
        'end_time': '2017-09-02',
        'limit': 10,
        'page': 1
    }
    sql_result = session.query(Task).filter(
        and_(
            # Order.user_id.like('%' + cond['user_id'] + '%') if cond['user_id'] is not None else "",
            # Task.task_do_time.between(cond['start_time'], cond['end_time']),
        ))
    sql_content = sql_result.order_by(Task.task_do_time).limit(cond['limit']).offset((cond['page'] - 1) * cond['limit'])
    sql_total = sql_result.count()
    result = [i.to_json() for i in sql_content]
    return result, sql_total


# 删除任务

def task_del():
    cond = {
        'task_id': 2
    }
    sql_result = session.query(Task).filter(Task.task_id == cond['task_id']).one()
    session.delete(sql_result)
    result = handler_commit(session)
    return result
