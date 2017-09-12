#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/9/8 14:21
"""
from sqlalchemy import (Column, Integer, String, ForeignKey)
from sqlalchemy.orm import relationship
from app.framework_api import date_time
from app.services import ModelBase
# <-元类


class Invoice(ModelBase):
    __tablename__ = "invoice"
    __table_args__ = {
        'mysql_auto_increment': '0000'
    }
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Integer, nullable=False)
    invoice_name = Column(String(100), nullable=False)
    company_num = Column(String(30), default="")
    tel = Column(String(30))
    person_address = Column(String(100))
    email = Column(String(30), default="")
    user_id = Column(Integer, ForeignKey('user.user_id'), primary_key=True)
    create_time = Column(String(length=50))

    def __init__(self, invoice_type, invoice_name, tel, person_address, user_id, email="", company_num=""):
        self.type = invoice_type
        self.invoice_name = invoice_name
        self.tel = tel
        self.person_address = person_address
        self.user_id = user_id
        self.email = email
        self.company_num = company_num
        self.create_time = date_time()

    def to_json(self):
        return {
            'id': self.id,
            'type': self.type,
            'tel': self.tel,
            'invoice_name': self.invoice_name,
            'person_address': self.person_address,
            'email': self.email,
            'company_num': self.company_num,
            'user_id': self.user_id,
            'create_time': self.create_time
        }

    def __repr__(self):
        return "<id={},type={},user_id={}>".format(self.id, self.type, self.user_id)