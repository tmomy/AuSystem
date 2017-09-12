#!/usr/bin/env python
# encoding: utf-8
"""
@author: leason
@time: 2017/9/8 14:09
"""

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy import ForeignKey
from app.services import ModelBase
from app.framework_api import date_time


class TypeNews(ModelBase):
    __tablename__ = "type_news"
    __table_args__ = {
        'mysql_auto_increment': '10001'
    }

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=50))
    index = Column(Integer)

    def __init__(self, name, index=0):
        self.name = name
        self.index = index

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'index': self.index
        }

    def __repr__(self):
        return "<id={},name={}>".format(self.id, self.name)


class News(ModelBase):
    __tablename__ = "news"
    __table_args__ = {
        'mysql_auto_increment': '10001'
    }

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_id = Column(Integer, ForeignKey('type_news.id', ondelete='CASCADE', onupdate='CASCADE'))
    pic = Column(String(length=150))
    model = Column(Integer, default=0)
    abstract = Column(String(length=250))
    title = Column(String(length=50))
    author = Column(String(length=50))
    source = Column(String(length=50))
    browser = Column(Integer, default=0)
    tag = Column(String(length=150))
    content = Column(Text)
    create_time = Column(DateTime, default=date_time())

    def __init__(self, type_id, pic, model,  abstract, title, author, source, tag, content):
        self.type_id = type_id
        self.title = title
        self.model = model
        self.abstract = abstract
        self.pic = pic
        self.author = author
        self.source = source
        self.tag = tag
        self.content = content

    def to_json(self):
        return {
            'id': self.id,
            'type_id': self.type_id,
            'title': self.title,
            'model': self.model,
            'abstract': self.abstract,
            'pic': self.pic,
            'author': self.author,
            'source': self.source,
            'browser': self.browser,
            'tag': self.tag,
            'create_time': str(self.create_time),
            'content': self.content
        }

    def __repr__(self):
        return "<id={},type_id={},title={}>".format(self.id, self.type_id, self.title)
