#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2017/9/4 8:55
"""
from ..NewaManageService import NewsOperate

# 新闻类型接口

service_news_type_add = NewsOperate.add_news_type
service_news_type_list = NewsOperate.list_news_type
service_news_type_del = NewsOperate.del_news_type
service_news_type_modify = NewsOperate.modify_news_type

# 新闻接口

service_news_add = NewsOperate.add_news
service_news_list = NewsOperate.list_news
service_news_del = NewsOperate.del_news
service_news_modify = NewsOperate.modify_news
service_news_detail = NewsOperate.detail_news


