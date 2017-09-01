#!/usr/bin/env python
# encoding: utf-8
"""
@author: XX
@time: 2017/8/30 15:47
"""
import sys

from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.Tables.product_attr import (AttrCategory, AttrInfo, SPUMapAttr)
from app.Tables.product import SPU, SKU, SKUMapAttr
from app.services import engine, handler_commit
reload(sys)
sys.setdefaultencoding('utf-8')
session = Session(engine)

# 获取属性集列表  attr_category
def get_attr_list(params):
    """
    #request:
    params = [1,2,3]   []查询所有属性及属性值
    #response::
    data = [
        {
            'attr_name': u'\u989c\u8272',
            'attr_id': 1,
            'value': [
                u'\u7ea2\u8272',
                u'\u767d\u8272'
            ]
        },
        {
            'attr_name': u'\u91cd\u91cf',
            'attr_id': 2,
            'value': [

            ]
        },
        {
            'attr_name': u'\u4e2a\u6570',
            'attr_id': 3,
            'value': [

            ]
        }
    ]
    """
    print type(params)
    if params:
        attr_list = session.query(AttrCategory).filter(AttrCategory.id.in_(params)).all()
    else:
        attr_list = session.query(AttrCategory).all()
    data = []
    for x in attr_list:
        attr_info_list = session.query(AttrInfo).filter(AttrInfo.attr_id == x.id).all()
        v_list = []
        for y in attr_info_list:
            v_list.append(y.attr_value)
        data.append({"attr_id": x.id, "attr_name": x.name, "value": v_list})
    return data

# 添加属性集及属性值 attr_category
def add_attr_set(params):
    """
    :request:
    params = [
        {
            "name": "重量",
            "value": ["1千克","5千克"]
        },{
            "name": "体积",
            "value": ["500ml","1L"]
        }
    ]
    :response:
    True
    """
    print params
    for item in params:
        attrCategory = session.query(AttrCategory).filter(AttrCategory.name == item["name"]).first()
        if attrCategory is None:
            attrCategory = AttrCategory(name=item["name"])
            session.add(attrCategory)
            session.flush()
        for x in item["value"]:
            if session.query(AttrInfo).filter(AttrInfo.attr_value == x).first():
                continue
            attr = AttrInfo(attr_id=attrCategory.id, attr_value= x)
            session.add(attr)
            session.flush()
    session.commit()
    return True


# 添加产品spu并选择产品属性    spu & spu_map_attr
def add_spu(params):
    """
    :request:
    params = {
        "name": "大白菜",
        "slogan": "白菜大降价 买二送一",
        "spu_NO": "2965432",
        "seller_id": "",
        "storage": 20,
        "attr_list": [2, 3]
    }
    :return:
    None
    """
    try:
        if session.query(SPU).filter(SPU.name == params["name"]).first():
            return False
        spu = SPU(name=params["name"], slogan=params["slogan"], spu_NO=params["spu_NO"], seller_id=params["seller_id"],
                  storage=params["storage"])
        session.add(spu)
        session.flush()
        for item in params["attr_list"]:
            spu_map_attr = SPUMapAttr(spu_id=spu.spu_id, attr_id=item)
            session.add(spu_map_attr)
        session.commit()
    except Exception:
        session.rollback()


# 编辑商品spu信息  为spu增加销售属性
def edit_spu(params):
    """
    :request:
    params = {
        "spu_id": 7,
        "name": "大白菜",
        "slogan": "白菜大降价 买二送一",
        "storage": 20,
        "attr_list": [2, 3, 4]   # 先删除 再增加
    }
    :response:
    None
    """
    try:
        # 查找所修改的spu id是否存在
        spu_find = session.query(SPU).filter(SPU.spu_id == params["spu_id"]).first()
        if spu_find:
            # 修改spu基本信息字段
            session.query(SPU).filter(SPU.spu_id == spu_find.spu_id).update({"name": params["name"],
                                                                             "slogan": params["slogan"],
                                                                             "storage": params["storage"]})
            session.flush()
            # 删除不需要的属性
            session.query(SPUMapAttr).filter(SPUMapAttr.spu_id == spu_find.spu_id,
                                             ~SPUMapAttr.attr_id.in_(params["attr_list"])).delete(synchronize_session=False)
            # 删除记录时，默认会尝试删除 session 中符合条件的对象，而 in 操作估计还不支持，于是就出错了。解决办法就是删除时不进行同步，然后再让 session 里的所有实体都过期
            session.commit()    # session.expire_all()
            # 查找该spu对应的sku_id
            sku_find = session.query(SKU).filter(SKU.spu_id == spu_find.spu_id).all()
            sku_list = []
            for x in sku_find:
                sku_list.append(x.sku_id)
            # 删除该spu下所有sku中属性被删掉的属性值
            session.query(SKUMapAttr).filter(SKUMapAttr.sku_id.in_(sku_list),
                                             ~SKUMapAttr.attr_id.in_((params["attr_list"]))).delete(synchronize_session=False)
            session.commit()
            # 将该spu新的属性集加入  如果存在就跳过
            for item in params["attr_list"]:
                if session.query(SPUMapAttr).filter(SPUMapAttr.spu_id == spu_find.spu_id,
                                                    SPUMapAttr.attr_id == item).first():
                    continue
                spu_attr = SPUMapAttr(attr_id=item, spu_id=spu_find.spu_id)
                session.add(spu_attr)
                session.flush()
            session.commit()
    except Exception:
        session.rollback()


# 添加产品sku     sku
def add_sku(params):
    """
    :request:
    params = {
            "spu_id": 1,
            "name": "plus",
            "price": 500,
            "storage": 20,
            "pic_url": "http://baidu.com",
            "sku_attr": [
                {
                    "attr_id": 1,
                    "attr_name": "颜色",
                    "attr_value": ["红色", "白色"]
                },{
                    "attr_id": 4,
                    "attr_name": "体积",
                    "attr_value": ["500ml", "1L", "2.5L"]
                }
            ]
        }
    :response: None
    """
    try:
        if session.query(SPU).filter(SPU.spu_id == params["spu_id"]).first():
            # if session.query(SKU).filter(SKU.name == params["name"]).first():
            #     print "SKU名称已存在"
            #     return False
            sku = SKU(name=params["name"], spu_id=params["spu_id"], price=params["price"], storage=params["storage"],pic_url=params["pic_url"])
            session.add(sku)
            session.flush()
            for x in params["sku_attr"]:
                for y in x["attr_value"]:
                    sku_attr = SKUMapAttr(sku_id=sku.sku_id, attr_id=x["attr_id"], attr_name=x["attr_name"], attr_value=y)
                    session.add(sku_attr)
                    session.flush()
            session.commit()
        else:
            return False
    except:
        session.rollback()


# 编辑sku
def edit_sku(params):
    """
    :request:
    params = {
            "sku_id": 7,
            "name": "plus",
            "price": 500,
            "storage": 20,
            "pic_url": "http://baidu.com",
            "sku_attr": [
                {
                    "attr_id": 1,
                    "attr_name": "颜色",
                    "attr_value": ["红色", "白色"]
                },{
                    "attr_id": 4,
                    "attr_name": "体积",
                    "attr_value": ["500ml", "1L", "2.5L"]
                }
            ]
        }
    :response:
     None
    """
    # 修改sku基本信息
    try:
        # 查找所修改的sku id是否存在
        sku_find = session.query(SKU).filter(SKU.sku_id == params["sku_id"]).first()
        if sku_find:
            # 修改spu基本信息字段
            session.query(SKU).filter(SKU.sku_id == sku_find.sku_id).update({"name": params["name"],
                                                                             "slogan": params["slogan"],
                                                                             "storage": params["storage"]})
            session.flush()
            # 修改sku_attr信息

            session.commit()
    except Exception:
        session.rollback()


if __name__=="__main__":
    # 获取属性集列表  attr_category
    # params = []
    # print get_attr_list(params)
    pass

    # 添加属性集及属性值
    # params = [
    #     {
    #         "name": "重量",
    #         "value": ["1千克", "5千克"]
    #     }, {
    #         "name": "体积",
    #         "value": ["500ml", "1L", "2.5L"]
    #     }
    # ]
    # print add_attr_set(params)
    pass

    # 添加产品spu
    # params = {
    #     "name": "大白菜11",
    #     "slogan": "白菜大降价 买二送一",
    #     "spu_NO": "2965432",
    #     "storage": 20,
    #     "attr_list": []
    # }
    # print add_spu(params)
    pass

    # 编辑spu信息 增加/去掉 销售属性
    # params = {
    #     "spu_id": 7,
    #     "name": "大白哈",
    #     "slogan": "白买二送二",
    #     "storage": 20,
    #     "attr_list": [2,  4, 5]
    # }
    # edit_spu(params)
    pass


    # 添加sku
    # params = {
    #         "spu_id": 7,
    #         "name": "plus",
    #         "price": 500,
    #         "storage": 20,
    #         "pic_url": "http://baidu.com",
    #         "sku_attr": [
    #             {
    #                 "attr_id": 1,
    #                 "attr_name": "颜色",
    #                 "attr_value": ["红色", "白色"]
    #             },{
    #                 "attr_id": 4,
    #                 "attr_name": "体积",
    #                 "attr_value": ["500ml", "1L", "2.5L"]
    #             }
    #         ]
    #     }
    # add_sku(params)
    pass

    # 编辑sku
    # params = {
    #         "sku_id": 7,
    #         "name": "plus",
    #         "price": 500,
    #         "storage": 20,
    #         "pic_url": "http://baidu.com",
    #         "sku_attr": [
    #             {
    #                 "attr_id": 1,
    #                 "attr_name": "颜色",
    #                 "attr_value": ["红色", "白色"]
    #             },{
    #                 "attr_id": 4,
    #                 "attr_name": "体积",
    #                 "attr_value": ["500ml", "1L", "2.5L"]
    #             }
    #         ]
    #     }
    # add_sku(params)
    pass






