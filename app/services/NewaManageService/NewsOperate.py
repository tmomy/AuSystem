#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2017/9/8 14:44
"""

import time, random, datetime
from app.framework_api import date_time
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.Tables.NewsModel import TypeNews, News

from .. import engine, handler_commit

session = Session(engine)


# 添加分类
def add_news_type(data):
    """
    :info
    @添加分类
    :request
    @data = {
        'name': '', 名称
        'index': 0  排序索引
    }
    :return: True or False
    """
    session.add(TypeNews(name=data['name'], index=data['index']))
    result = handler_commit(session)
    session.close()
    return result[0]


# 编辑分类
def modify_news_type(cond):
    """
    :info
    @编辑分类
    :request
    @cond = {
        'id': '', id
        'name': '', 名称
        'index': 0  排序索引
    }
    :return: True or False
    """
    id = cond['id']
    name = cond['name']
    index = cond['index']
    sql_result = session.query(TypeNews).filter(TypeNews.id == id)
    if sql_result.count() is 1:
        sql_result.one().name = name
        sql_result.one().index = str(index)
        result = handler_commit(session)[0]
    else:
        result = False
    session.close()
    return result


# 删除分类
def del_news_type(id):
    """
    :info
    @删除分类
    :request
    @id=2255
    :return: True or False
    """
    sql_result = session.query(TypeNews).filter(TypeNews.id == id)
    if sql_result.count() is 1:
        session.delete(sql_result.one())
        result = handler_commit(session)[0]
    else:
        result = False
    session.close()
    return result


# 获取分类
def list_news_type():
    """
    :info
    @获取分类
    :request
    @None
    :return: result and total
    """
    sql_result = session.query(TypeNews).all()
    result = [i.to_json() for i in sql_result]
    total = len(result)
    session.close()
    return result, total


# 添加新闻
def add_news(cond):
    """
    :info
    @添加新闻
    :request
    @cond = {
        'type_id': 123434,
        'pic': '/img/1.jpg',
        'model': 0,
        'abstract': 'xxxx',
        'title': 'hello',
        'author': 'leason',
        'source': 'baidu.com',
        "tag":"aaaa,bbbb",
        'browser': 236,
        'content': 'xxx',
        'index': 0
    }
    :return: True or False
    """
    session.add(News(type_id=cond['type_id'], model=cond['model'], abstract=cond['abstract'], pic=cond['pic'], title=cond['title'], author=cond['author'], source=cond['source'], tag=cond['tag'], content=cond['content']))
    result = handler_commit(session)
    session.close()
    return result[0]


# 编辑新闻
def modify_news(cond):
    """
    :info
    @编辑新闻
    :request
    @cond = {
        'id': '',
        'type_id': 123434,
        'pic': '/img/1.jpg',
        'model': 0,
        'abstract': 'xxxx',
        'title': 'hello',
        'author': 'leason',
        'source': 'baidu.com',
        'browser': 236,
        'content': 'xxx',
        'index': 0
    }
    :return: True or False
    """
    id = cond['id']
    sql_result = session.query(News).filter(News.id == id)
    if sql_result.count() is 1:
        result_content = sql_result.one()
        result_content.content = cond['content']
        result_content.type_id = cond['type_id']
        result_content.abstract = cond['abstract']
        result_content.pic = cond['pic']
        result_content.model = cond['model']
        result_content.title = cond['title']
        result_content.author = cond['author']
        result_content.source = cond['source']
        result = handler_commit(session)[0]
    else:
        result = False
    session.close()
    return result


# 删除新闻
def del_news(id):
    """
    :info
    @删除新闻
    :request
    @id=2255
    :return: True or False
    """
    sql_result = session.query(News).filter(News.id == id)
    if sql_result.count() is 1:
        session.delete(sql_result.one())
        result = handler_commit(session)[0]
    else:
        result = False
    session.close()
    return result


# 获取新闻
def list_news(data):
    """
    :info
    @新闻组合查询
    :request
    @cond = {
        'cond':{
            'title': '',
            'type_id': '',
            'sort': 0      0 1 2 时间 访问量高 访问量低
        },
        'limit': 10,
        'page': 1
    }
    :return: result or total
    """
    limit = data['limit']
    offset = (data['page'] - 1) * data['limit']
    title = data['cond']['title']
    type_id = data['cond']['type_id']
    # 排序类型
    switcher = {
        0: News.create_time.desc(),
        1: News.browser,
        2: News.browser.desc()
    }
    if data['cond']['sort']:
        sort_type = switcher[data['cond']['sort']]
    else:
        sort_type = switcher[0]

    sql_result = session.query(News, TypeNews.name).join(TypeNews, isouter=True).filter(
        and_(
            News.title.like('%' + str(title) + '%') if title is not None else "",
            News.type_id.like('%' + str(type_id) + '%') if type_id is not None else ""
        ))
    sql_content = sql_result.order_by(sort_type).limit(limit).offset(offset)
    sql_total = sql_result.count()
    handler_commit(session)
    session.close()
    result = [dict(i[0].to_json().items() + {'type_name': i[1]}.items()) for i in sql_content]
    return result, sql_total


# 获取新闻详情
def detail_news(id):
    """
    :info
    @新闻详情
    :request
    @id=2255
    :return: True or False
    """
    sql_result = session.query(News, TypeNews.name).join(TypeNews, isouter=True).filter(News.id == id)
    if sql_result.count() is 1:
        result_content = sql_result.one()
        result = dict(result_content[0].to_json().items() + {'type_name': result_content[1]}.items())
        result_content[0].browser += 1
        handler_commit(session)
    else:
        result = False
    session.close()

    return result