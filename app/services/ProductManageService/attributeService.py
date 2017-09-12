#!/usr/bin/env python
# encoding: utf-8
"""
@author: XX
@time: 2017/9/1 10:21
"""
import sys

from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.Tables.ProductAttrModel import (AttrCategory, AttrInfo, SPUMapAttr)
from app.Tables.ProductModel import SPU, SKU, SKUMapAttr
from app.services import engine, handler_commit, err_logging
from app.conf import msg
reload(sys)
sys.setdefaultencoding('utf-8')
session = Session(engine)


# 获取属性集列表  attr_category
@err_logging
def get_attr_list(params):
    """
    #request:
    params = [1,2,3]   []查询所有属性及属性值
    #response::
    data = [
    ]
    """
    if params:
        attr_list = session.query(AttrCategory).filter(AttrCategory.id.in_(params)).all()
    else:
        attr_list = session.query(AttrCategory).all()
    data = []
    for x in attr_list:
        attr_info_list = session.query(AttrInfo).filter(AttrInfo.attr_id == x.id).all()
        v_list = []
        for y in attr_info_list:
            v_list.append({"id": y.id, "attr_value": y.attr_value})
        data.append({"attr_id": x.id, "attr_name": x.name, "value": v_list})
    return data


# 添加属性集及属性值 attr_category
@err_logging
def add_attr_set(params):
    """
    :request:
    params = {
        "name": "体积",
        "value": {
                "0": "2L",
                "1": "4L"
            }
    }
    :response:
    True
    """
    attrCategory = session.query(AttrCategory).filter(AttrCategory.name == params["name"]).first()
    if attrCategory is None:
        attrCategory = AttrCategory(name=params["name"])
        session.add(attrCategory)
        session.flush()
    for x in params["value"]:
        if session.query(AttrInfo).filter(AttrInfo.attr_value == params["value"][x],
                                          AttrInfo.attr_id == attrCategory.id).first():
            continue
        attr = AttrInfo(attr_id=attrCategory.id, attr_value=params["value"][x])
        session.add(attr)
    handler_commit(session)
    return True, msg.ERROR(0, "添加成功")


@err_logging
def del_attr(params):
    """
    params = {
        "id": 4
    }
    :param params:
    :return:
    """
    attr = session.query(AttrCategory).filter(AttrCategory.id == params["id"]).one_or_none()
    if attr:
        session.delete(attr)
        handler_commit(session)
        return True, msg.ERROR(0, "删除成功")
    else:
        return False, msg.ERROR(1, "删除失败，属性不存在")

# 属性值的删除 attr_info
@err_logging
def del_attr_info(params):
    attr_info = session.query(AttrInfo).filter(AttrInfo.id == params["id"]).first()
    if attr_info:
        session.delete(attr_info)
        handler_commit(session)
        return True, msg.ERROR(0, "删除成功")
    else:
        return False, msg.ERROR(1, "删除失败，属性值不存在")


# 添加产品spu并选择产品属性    spu & spu_map_attr
@err_logging
def add_spu(params):
    """
    :request:
    params = {
        "name": "大白菜",
        "slogan": "白菜大降价 买二送一",
        "origin": "产地",
        "seller_id": "",
        "storage": 20,
        "category_id": 4,
        "attr_list": [2, 3]
    }
    :return:
    None
    """
    if session.query(SPU).filter(SPU.name == params["name"]).first():
        return False, msg.ERROR(1, "添加失败")
    spu = SPU(name=params["name"], slogan=params["slogan"], origin=params["origin"], seller_id=params["seller_id"],
              storage=params["storage"], category_id=params["category_id"])
    session.add(spu)
    session.flush()
    for item in params["attr_list"]:
        spu_map_attr = SPUMapAttr(spu_id=spu.spu_id, attr_id=item)
        session.add(spu_map_attr)
    handler_commit()
    return True, msg.ERROR(0, "添加成功")

