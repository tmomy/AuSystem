#!/usr/bin/env python
# encoding: utf-8
"""
@author: XX
@time: 2017/8/30 15:47
"""
import sys
from app.Tables.CategoryModel import Category
from app.conf import msg
from sqlalchemy.orm import Session
from app.Tables.ProductAttrModel import (AttrCategory, AttrInfo, SPUMapAttr)
from app.Tables.ProductModel import SPU, SKU, SKUMapAttr
from app.services import engine, handler_commit
reload(sys)
sys.setdefaultencoding('utf-8')
session = Session(engine)


# 获取商品spu列表
def product_spu_list(params):
    """
    :request:
    params = {
        "opr": "search",
        "data": {
            "page": 1,
            "limit": 3,
            "cond": {
                "category_id": 1,
                "name": "苹果"
            }
        }
    }
    :return:
    data = {
        "count": n,
        "data": []
    }
    """
    data = []
    cate_id_list = [x for x in find_prodcut_by_cate_id(params["cond"]["category_id"]).split(',') if x != '']
    if params["cond"]["name"]:
        spu_find = session.query(SPU).filter(SPU.name.like('%' + params["cond"]["name"] + '%'),
                                             SPU.category_id.in_(cate_id_list)).order_by(SPU.create_time.desc())
    else:
        spu_find = session.query(SPU).filter(SPU.category_id.in_(cate_id_list)).order_by(SPU.create_time.desc())
    count = spu_find.count()
    spu_list = spu_find.offset((params["page"]-1)*params["limit"]).limit(params["limit"]).all()
    for item in spu_list:
        spu_attr = get_spu_attr(item.spu_id)
        category = session.query(Category).filter(Category.category_id == item.category_id).one_or_none()
        if category:
            cate_name = category.name
        data.append({"spu_id": item.spu_id,
                     "slogan": item.slogan,
                     "seller_id": item.seller_id,
                     "origin": item.origin,
                     "name": item.name,
                     "create_time": item.create_time,
                     "category_id": item.category_id,
                     "cate_name": cate_name,
                     "storage": item.storage,
                     "spu_attr": spu_attr})
    return data, count


# 添加产品spu 及属性
def add_spu(params):
    """
    params = {
        "name": "",
        "slogan": "",
        "origin": "",
        "seller_id": "",
        "storage": 10,
        "category_id": "",
        "attr_str": "10001,10006"
    }
    :param params:
    :return:
    """
    spu = SPU(name=params["name"], slogan=params["slogan"], origin=params["origin"], seller_id=params["seller_id"],
              storage=params["storage"], category_id=params["category_id"])
    session.add(spu)
    session.flush()
    attr_list = params["attr_str"].split(",")
    for item in attr_list:
        spu_attr = SPUMapAttr(attr_id=item, spu_id=spu.spu_id)
        session.add(spu_attr)
        session.flush()
    handler_commit(session)


# 编辑商品spu基本信息 或 添加属性
def edit_spu(params):
    """
    :request:
    params = {
        "spu_id": 7,
        "name": "大白菜",
        "slogan": "白菜大降价 买二送一",
        "storage": 20,
        "seller_id": "",
        "origin": "河南",
        "attr_str": "10001,10006"
    }
    :response:
    None
    """
    # 查找所修改的spu id是否存在
    spu_find = session.query(SPU).filter(SPU.spu_id == params["spu_id"]).first()
    if spu_find:
        # 修改spu基本信息字段
        session.query(SPU).filter(SPU.spu_id == spu_find.spu_id).update({"name": params["name"],
                                                                         "slogan": params["slogan"],
                                                                         "origin": params["origin"],
                                                                         "seller_id": params["seller_id"],
                                                                         "storage": params["storage"]})
        attr_list = params["attr_str"].split(",")
        for item in attr_list:
            if session.query(SPUMapAttr).filter(SPUMapAttr.attr_id == item,
                                                SPUMapAttr.spu_id == spu_find.spu_id).first():
                continue
            else:
                spu_attr = SPUMapAttr(attr_id=item, spu_id=spu_find.spu_id)
                session.add(spu_attr)
        handler_commit(session)
        return True, msg.ERROR(0, "添加成功")
    else:
        return False, msg.ERROR(1, "添加失败")


# 删除spu关联属性
def del_spu_attr(params):
    """
    params = {
        "opr": "delete",
        "data": {
            "spu_id"： 10001,
            "attr_id": 10001
        }
    }
    :param params:
    :return:
    """
    spu_attr_find = session.query(SPUMapAttr).filter(SPUMapAttr.spu_id == params["spu_id"],
                                                     SPUMapAttr.attr_id == params["attr_id"]).first()
    if spu_attr_find:
        session.query(SPUMapAttr).filter(SPUMapAttr.spu_id == params["spu_id"],
                                         SPUMapAttr.attr_id == params["attr_id"]).delete()
        handler_commit(session)
        return True, msg.ERROR(0, "删除成功")
    else:
        return False, msg.ERROR(1, "删除失败")


# 删除spu信息
def del_spu(params):
    """
    params = {
        "id": 2
    }
    :param params:
    :return:
    """
    spu_find = session.query(SPU).filter(SPU.spu_id == params["id"]).one_or_none()
    if spu_find:
        session.delete(spu_find)
        handler_commit(session)
        return True, msg.ERROR(0, "删除成功")
    else:
        return False, msg.ERROR(1, "删除失败")


# 获取某商品所有属性
def get_spu_attr(spu_id):
    spu_find = session.query(SPU).filter(SPU.spu_id == spu_id).one_or_none()
    if spu_find:
        attr_list = []
        attr_find = session.query(SPUMapAttr).filter(SPUMapAttr.spu_id == spu_id).all()
        for item in attr_find:
            attr = session.query(AttrCategory).filter(AttrCategory.id == item.attr_id).one_or_none()
            attr_list.append(attr.to_json())
        return attr_list
    else:
        return []


# 获取某商品所有属性及属性值
def get_product_attr(spu_id):
    import time
    time.sleep(1)
    spu_find = session.query(SPU).filter(SPU.spu_id == spu_id).one_or_none()
    if spu_find:
        attr_list = []
        attr_find = session.query(SPUMapAttr).filter(SPUMapAttr.spu_id == spu_id).all()
        for item in attr_find:
            attr = session.query(AttrCategory).filter(AttrCategory.id == item.attr_id).one_or_none()
            attr_info_find = session.query(AttrInfo).filter(AttrInfo.attr_id == attr.id).all()
            attr_value_list = []
            for x in attr_info_find:
                attr_value_list.append({"id": x.id, "attr_value": x.attr_value})
            attr_list.append({"id": attr.id, "name": attr.name, "value": attr_value_list})
        return attr_list
    else:
        return []


# 获取某商品所有sku
def get_sku_list(params):
    """
    params = {
        "opr": "search",
        "data": {
            "page": 1,
            "limit": 3,
            "cond": {
                "spu_id": 10012
            }
        }
    }
    :param params:
    :return:
    """
    sku_find = session.query(SKU).filter(SKU.spu_id == params["cond"]["spu_id"])
    sku_list = []
    total = sku_find.count()
    sku_find = sku_find.offset((params["page"]-1)*params["limit"]).limit(params["limit"]).all()
    if sku_find:
        for x in sku_find:
            attr_list = get_sku_attr(x.sku_id)
            sku = {"sku_id": x.sku_id, "name": x.name, "storage": x.storage, "price": x.price, "pic_url": x.pic_url,
                   "create_time": x.create_time, "attr_list": attr_list}
            sku_list.append(sku)
        return sku_list, total


# 添加产品sku
def add_sku(params):
    """
    :request:
    params = {
            "spu_id": 1,
            "name": "plus",
            "price": 500,
            "storage": 20,
            "pic_url": "http://baidu.com",
            "sku_attr": "10001,10002,10015,10020,10021,10022"
        }
    :response: None
    """
    if session.query(SPU).filter(SPU.spu_id == params["spu_id"]).first():
        sku = SKU(name=params["name"], spu_id=params["spu_id"], price=params["price"], storage=params["storage"],
                  pic_url=params["pic_url"])
        session.add(sku)
        session.flush()
        sku_attr = params["sku_attr"].split(",")
        for x in sku_attr:
            sku_map_attr = SKUMapAttr(sku_id=sku.sku_id, attr_info_id=x)
            session.add(sku_map_attr)
        handler_commit(session)
        return True, msg.ERROR(0, "添加成功")
    else:
        return False, msg.ERROR(1, "添加失败")


# 获取某sku所有属性及属性值
def get_sku_attr(sku_id):
    sku_attr_find = session.query(SKUMapAttr).filter(SKUMapAttr.sku_id == sku_id).all()
    attr_info_list = []
    for x in sku_attr_find:
        attr_info_find = session.query(AttrInfo).filter(AttrInfo.id == x.attr_info_id).one_or_none()
        if attr_info_find:
            attr_info_list.append(attr_info_find)
    attr_id = set()
    for y in attr_info_list:
        attr_id.add(y.attr_id)
    result =[]
    for z in attr_id:
        attr_str = []
        for m in attr_info_list:
            if z == m.attr_id:
                attr_str.append({"id": m.id, "attr_value": m.attr_value})
            attr_name = session.query(AttrCategory).filter(AttrCategory.id == z).one_or_none()
        attr = {"attr_id": z, "attr_name": attr_name.name, "attr_value": attr_str}
        result.append(attr)
    return result


# 编辑sku基本信息
def edit_sku(params):
    """
    :request:
    params = {
            "sku_id": 7,
            "name": "plus",
            "price": 500,
            "storage": 20,
            "pic_url": "http://baidu.com",
            "sku_attr": "10001,10002,10015,10020,10021,10022"
        }
    :response:
     None
    """
    # 查找所修改的sku id是否存在
    sku_find = session.query(SKU).filter(SKU.sku_id == params["sku_id"]).first()
    if sku_find:
        # 修改spu基本信息字段
        session.query(SKU).filter(SKU.sku_id == sku_find.sku_id).update({"name": params["name"],
                                                                         "price": params["price"],
                                                                         "storage": params["storage"],
                                                                         "pic_url": params["pic_url"]})
        sku_attr = params["sku_attr"].split(",")
        for x in sku_attr:
            if session.query(SKUMapAttr).filter(SKUMapAttr.sku_id == sku_find.sku_id,
                                                SKUMapAttr.attr_info_id == x).first():
                continue
            else:
                sku_map_attr = SKUMapAttr(sku_id=params["sku_id"], attr_info_id=x)
                session.add(sku_map_attr)
        handler_commit(session)
        return True, msg.ERROR(0, "修改成功")
    else:
        return False, msg.ERROR(1, "修改失败")


# 删除某sku
def del_sku(params):
    """
    params = {
        "sku_id": n
    }
    :param params:
    :return:
    """
    sku = session.query(SKU).filter(SKU.sku_id == params["sku_id"]).one_or_none()
    if sku:
        session.delete(sku)
        handler_commit(session)
        return True, msg.ERROR(0, "删除成功")
    else:
        return False, msg.ERROR(1, "删除失败")


# 删除sku属性
def del_sku_attr(params):
    """
    params = {
        "opr": "delete",
        "data": {
            "sku_id": n,
            "id": n
        }
    }
    :param params:
    :return:
    """
    sku_attr_find = session.query(SKUMapAttr).filter(SKUMapAttr.sku_id == params["sku_id"],
                                                     SKUMapAttr.attr_info_id == params["id"]).first()
    if sku_attr_find:
        session.query(SKUMapAttr).filter(SKUMapAttr.sku_id == params["sku_id"],
                                         SKUMapAttr.attr_info_id == params["id"]).delete()
        handler_commit(session)
        return True, msg.ERROR(0, "删除成功")
    else:
        return False, msg.ERROR(1, "删除失败")


# 根据category_id查询所有子分类
def find_prodcut_by_cate_id(category_id):
    child_list = ''
    category = session.query(Category).filter(Category.category_id == category_id).first()
    childs = category.children
    if not len(childs):
        return category_id
    else:
        for child in childs:
            if child.category_id == category_id:
                data = child.category_id
            else:
                if find_prodcut_by_cate_id(child.category_id):
                    data = find_prodcut_by_cate_id(child.category_id)
            child_list += (str(data) + ",")
    handler_commit(session)
    return child_list
