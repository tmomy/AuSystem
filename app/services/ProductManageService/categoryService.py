#!/usr/bin/env python
# encoding: utf-8
"""
@author: XX
@time: 2017/9/1 10:22
"""
import sys

from sqlalchemy import func
from sqlalchemy import or_, distinct
from sqlalchemy.orm import Session
from app.Tables.CategoryModel import Category
from app.services import engine, handler_commit, err_logging
from app.framework_api import redis_service
from app.conf import msg
reload(sys)
sys.setdefaultencoding('utf-8')
session = Session(engine)

category_list = []


# 获取某种类子分类
def category_child(params):
    """
    params= {
        "category_id": ""
    }
    :return:
    data = [
        {
            'parent_id': 2,
            'category_id': 7,
            'name': u'\u74dc'
        },
        {
            'parent_id': 2,
            'category_id': 8,
            'name': u'\u679c'
        }
    ]
    """
    child_level = session.query(Category).filter(Category.parent_id == params["category_id"],
                                                 Category.category_id != params["category_id"]).all()
    data = []
    if child_level:
        for x in child_level:
            data.append(x.to_json())
        return data
    else:
        return False, msg.ERROR(1, "查询失败")


# 添加种类
@err_logging
def category_add(params):
    """
    :request:
    params = {
            "name": "瓜果",
            "parent_id": 1, # 基类id为1
            "sn": 5
        }
    :response:
    None
    """
    category = session.query(Category).filter(Category.name == params["name"],
                                              Category.parent_id == params["parent_id"]).first()
    if category is None:
        cate_new = Category(name=params["name"], parent_id=params["parent_id"], sn=params["sn"])
        session.add(cate_new)
        handler_commit(session)
        return True, msg.ERROR(0, "添加成功")
    else:
        return False, msg.ERROR(1, "添加失败")


# 删除一个种类
@err_logging
def category_del(category_id):
    """
    :request:
    params = {
            "category_id" : 3
        }
    :response:
    None
    """
    if category_id == 1:
        return False, msg.ERROR(1, "删除失败")
    else:
        category = session.query(Category).filter(Category.category_id == category_id).first()
        session.delete(category)
        handler_commit(session)
        cate_find = session.query(Category).filter(Category.parent_id == category.category_id).all()
        for item in cate_find:
            category_del(item.category_id)
        return True, msg.ERROR(0, "删除成功")


@err_logging
def get_category_tree():
    search_cate = session.query(Category).with_lockmode('read').filter(Category.category_id == 1).one_or_none()
    handler_commit(session)
    return [{"value": search_cate.category_id, "label": search_cate.name, "sn": search_cate.sn,
            "children": get_category(search_cate.category_id)}]


@err_logging
def get_category(category_id=1):
    child_list = []
    search_cate = session.query(Category).filter(Category.category_id == category_id).one_or_none()
    childs = search_cate.children
    if not len(childs):
        child_list = []
    else:
        for child in childs:
            if child.category_id != category_id:
                data = {
                    "value": child.category_id,
                    "label": child.name,
                    'sn': child.sn,
                    "children": get_category(child.category_id)
                }
                if not data["children"]:
                    data = {
                        "value": child.category_id,
                        "label": child.name,
                        'sn': child.sn
                    }
                child_list.append(data)
            else:
                pass
    session.close()
    sort_list = sorted(child_list, key=lambda x: x['sn'], reverse=False)
    return sort_list


# 获取所有分类列表  非树形式
@err_logging
def get_category_table(params):
    import time
    time.sleep(1)
    cate_list = []
    category = session.query(Category).with_lockmode('read')
    total = category.count()
    for item in category.offset((params["page"]-1)*params["limit"]).limit(params["limit"]):
        cate_list.append(item.to_json())
    handler_commit(session)
    return cate_list, total


def category_edit(params):
    """
    params = {
        "opr" : "edit",
        "data": {
            "category_id": n,
            "name": "",
            "sn": ""
        }
    }
    :param params:
    :return:
    """
    category = session.query(Category).filter(Category.category_id == params["category_id"]).one_or_none()
    if category:
        session.query(Category).filter(Category.category_id == params["category_id"]).update(
            {Category.name: params["name"], Category.sn: params["sn"]})
        handler_commit(session)
        return True, msg.ERROR(0, "修改成功")
    else:
        return False, msg.ERROR(1, "修改失败")












