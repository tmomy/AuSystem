#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2017/8/31 10:10
"""
import time, datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.Tables.TaskModel import Task
from app.Tables.userModel import User
from .. import engine, handler_commit

session = Session(engine)


# 新增任务

def task_add(data):
    """
    :info
    @该用户是否存在记录 存在则覆盖 不存在新增
    @并且对将task_num=1的进行处理 有则删掉 无则不处理
    @增加要检查用户余额，是否足够增加
    :request
    @data = {
        'user_id': '',
        'tasks': [
            {'task_num': 2, 'task_do_time': '2017-09-01'},
            {'task_num': 0, 'task_do_time': '2017-09-02'},
            {'task_num': 3, 'task_do_time': '2017-09-03'}
        ]
    }
    :return: True or False
    """
    try:
        local_date_str = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        # 默认截止时间3000年以后
        end_date_str = datetime.date.today().replace(3000).strftime('%Y-%m-%d')
        local_date = datetime.datetime.strptime(time.strftime('%Y-%m-%d', time.localtime(time.time())), "%Y-%m-%d")
        for task in data['tasks']:
            task_time = datetime.datetime.strptime(task['task_do_time'], "%Y-%m-%d")
            task_result = session.query(Task).filter(
                and_(
                    Task.user_id == data['user_id'],
                    Task.task_do_time == task['task_do_time']
                ))
            # 用户余额 - 当前时间到最后的记录 所有的task_num的和 = 可操作的数额
            rest_day = session.query(User).filter(
                and_(
                    User.user_id == data['user_id']
                )).one().rest_day
            task_result_total = session.query(Task).filter(
                and_(
                    Task.user_id == data['user_id'],
                    Task.task_do_time.between(local_date_str, end_date_str),
                ))

            if task_result.count() is not 0:
                task_result_sum = sum([a.task_num for a in task_result_total])
                last_task = datetime.datetime.strptime(str(task_result_total.order_by(Task.task_do_time.desc()).first().task_do_time),
                                               "%Y-%m-%d %H:%M:%S")
                add_day = last_task - local_date
                # 剩余天数 - 已有任务task_num总和 - 最后一个任务和当前时间的差 + 已有任务数量 + 当天已存在任务的数量
                free_day = rest_day - task_result_sum - add_day.days + task_result_total.count() + task_result.one().task_num
                # print rest_day
                # print task_result_sum
                # print add_day.days
                # print task_result_total.count()
                # print task_result.one().task_num
                # print free_day
                if free_day < task['task_num']:
                    session.rollback()
                    return False
                else:
                    if task['task_num'] is 1:
                        session.delete(task_result.one())
                    else:
                        task_result.one().task_num = task['task_num']

            else:
                if task['task_num'] is not 1:
                    # 检查余额  可操作的数额 > task['task_num']
                    if task_result_total.count() > 0:
                        task_result_sum = sum([a.task_num for a in task_result_total])
                        last_task = datetime.datetime.strptime(
                            str(task_result_total.order_by(Task.task_do_time.desc()).first().task_do_time),
                            "%Y-%m-%d %H:%M:%S")
                        add_day = last_task - local_date
                        # 剩余天数 - 已有任务task_num总和 - 最后一个任务和当前时间的差 + 已有任务数量
                        free_day = rest_day - task_result_sum - add_day.days + task_result_total.count()
                        # 当新建任务在最后任务之后 free_day-超过的天数
                        if (task_time - last_task).days > 0:
                            free_day = free_day - (task_time - last_task).days
                    else:
                        free_day = rest_day - (task_time - local_date).days

                    if free_day >= task['task_num']:
                        session.add(Task(user_id=data['user_id'], task_num=task['task_num'], task_do_time=task['task_do_time']))
                    else:
                        session.rollback()
                        return False

        result = handler_commit(session)
    except Exception:
        session.rollback()
        result = False
    return result


# 查询任务

def task_list(data):
    """
    :info
    @根据用户id和时间查询
    :request
    @data = {
        'cond':{
            'user_id': '',
            'start_time': '2017-09-01',
            'end_time': '2017-09-02'
        }
        'limit': 10,
        'page': 1
    }
    :return:
    @result=[]
    @sql_total=0
    """
    cond = data['cond']
    sql_result = session.query(Task).filter(
        and_(
            Task.user_id.like('%' + cond['user_id'] + '%') if cond['user_id'] is not None else "",
            Task.task_do_time.between(cond['start_time'], cond['end_time']),
        ))
    sql_content = sql_result.order_by(Task.task_do_time).limit(data['limit']).offset((data['page'] - 1) * data['limit'])
    sql_total = sql_result.count()
    result = [i.to_json() for i in sql_content]
    return result, sql_total


# 删除任务

def task_del():
    """
    :info
    @根据task_id删除
    :request
    @cond = {
        'task_id': 2
    }
    :return: True or False
    """
    cond = {
        'task_id': 2
    }
    try:
        sql_result = session.query(Task).filter(Task.task_id == cond['task_id']).one()
        session.delete(sql_result)
        result = handler_commit(session)
    except Exception:
        session.rollback()
        result = False
    return result
