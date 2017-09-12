#!/usr/bin/env python
# encoding: utf-8
"""
@author: XX
@time: 2017/9/5 11:21
"""
from ..ProductManageService import productService, attributeService, categoryService

# 分类接口
service_category_add = categoryService.category_add
service_category_tree = categoryService.get_category_tree
service_category_table = categoryService.get_category_table
service_category_delete = categoryService.category_del
service_category_edit = categoryService.category_edit
service_category_getOne = categoryService.category_child


# 属性管理
service_attribute_add = attributeService.add_attr_set
service_attribute_delete_value = attributeService.del_attr_info
service_attribute_delete_attr = attributeService.del_attr
service_attribute_search = attributeService.get_attr_list


# 产品管理
# spu
service_spu_search = productService.product_spu_list
service_spu_edit = productService.edit_spu
service_spu_delete = productService.del_spu
service_spu_add = productService.add_spu

# spu_attr
service_spu_attr_delete = productService.del_spu_attr
service_spu_attr_search = productService.get_spu_attr

# sku
service_sku_search = productService.get_sku_list
service_sku_edit = productService.edit_sku
service_sku_add = productService.add_sku
service_sku_delete = productService.del_sku

# sku_attr
service_product_attr_get = productService.get_product_attr
service_sku_attr_delete = productService.del_sku_attr



