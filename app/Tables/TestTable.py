# #!/usr/bin/env python
# # encoding: utf-8
# # """
# # @author: WL
# # @time: 2017/8/29 10:11
# # """
# from sqlalchemy import (Column, Integer, String, DateTime, ForeignKey, PrimaryKeyConstraint)
# from sqlalchemy.orm import relationship, Session
# from sqlalchemy.schema import Sequence
# from sqlalchemy.ext.declarative import declarative_base
# from functools import wraps
# from app.mysql_db import db_pool
# import traceback
#
# ModelBase = declarative_base()
# engine = db_pool
# session = Session(engine)
# # # <-元类
#
#
# class Role(ModelBase):
#     __tablename__ = "t_roles"
#     role_id = Column(Integer, primary_key=True)
#     name = Column(String(length=30), unique=True)
#     enable = Column(Integer)
#     cate_time = Column(String(length=50))
#     area_set = relationship("RoleRoute",cascade="save-update, delete", backref='t_roles')
#
#     def __init__(self, role_name, enable=0):
#         self.name = role_name
#         self.enable = enable
#
#     def to_json(self):
#         return {
#             'id': self.role_id,
#             'name': self.name,
#             'enable': self.enable,
#             'cate_time': self.cate_time
#         }
#
#     def __repr__(self):
#         return "<id={},role_name={},enable={}>".format(self.role_id, self.name, self.enable)
#
#
# class Route(ModelBase):
#     __tablename__ = "t_routes"
#     route_id = Column(Integer, primary_key=True)
#     rule = Column(String(length=255), unique=True)
#     name = Column(String(length=30))
#     add = Column(Integer, default=-1)
#     modify = Column(Integer, default=-1)
#     delete = Column(Integer, default=-1)
#     search = Column(Integer, default=-1)
#
#     def __init__(self, rule, name, *args):
#         self.rule = rule
#         self.name = name
#         if "add" in args:
#             self.add = 0
#         if "modify" in args:
#             self.modify = 0
#         if "delete" in args:
#             self.delete = 0
#         if "search" in args:
#             self.search = 0
#
#     def to_json(self):
#         return {
#             'id': self.route_id,
#             'rule': self.rule,
#             'name': self.name,
#             'add': self.add,
#             'modify': self.modify,
#             'delete': self.delete,
#             'search': self.search
#         }
#
#     def __repr__(self):
#         return "<id={},rule={},name={},add={},modify={},delete={},search={}>".format(self.route_id, self.rule, self.name,
#                                                                                      self.add, self.modify, self.delete,
#                                                                                      self.search)
#
#
# class RoleRoute(ModelBase):
#     __tablename__ = "role_pk_route"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     role_id = Column(Integer, ForeignKey('t_roles.role_id'), primary_key=True)
#     route_id = Column(Integer, ForeignKey('t_routes.route_id'), primary_key=True)
#     route_name = Column(String(length=30))
#     rule = Column(String(length=255))
#     add = Column(Integer, default=-1)
#     modify = Column(Integer, default=-1)
#     delete = Column(Integer, default=-1)
#     search = Column(Integer, default=-1)
#
#     def __init__(self, route):
#         self.modify = route.modify
#         self.search = route.search
#         self.delete = route.delete
#         self.route_name = route.name
#         self.route = route
#         self.rule = route.rule
#         self.add = route.add
#
#     def to_json(self):
#         return {
#             'id': self.id,
#             'route_id': self.route_id,
#             'role_id': self.role_id,
#             'rule': self.rule,
#             'name': self.name,
#             'add': self.add,
#             'modify': self.modify,
#             'delete': self.delete,
#             'search': self.search
#         }
#     route = relationship(Route)
#
#
# if __name__ == '__main__':
#     ModelBase.metadata.drop_all(bind=engine)
#     ModelBase.metadata.create_all(bind=engine)
#     role1 = Role(role_name='哈哈1')
#     role2 = Role(role_name='哈哈2')
#     # # user = session.query(User).first()
#     rule1 = RoleRoute(Route(rule ='规则1',name="1"))
#     rule2 = RoleRoute(Route(rule ='规则2',name="2"))
#     rule3 = RoleRoute(Route(rule ='规则3',name="2"))
#     rule4 = RoleRoute(Route(rule ='规则4',name="1"))
#     role1.area_set.append(rule1)
#     role2.area_set.append(rule1)
#     role1.area_set.append(rule2)
#     role2.area_set.append(rule2)
#     role1.area_set.append(rule3)
#     role2.area_set.append(rule3)
#     role1.area_set.append(rule4)
#     role2.area_set.append(rule4)
#     session.add(role1)
#     session.commit()
#     # # user.blog_list = [blog]
#     # user.blog_list_auto.append(blog)
#     # # session.delete(user)
#     session.add(role2)
#     session.commit()
#     # role2 = session.query(Role).filter(Role.role_id == 1).first()
#     # r = session.query(Route).filter(Route.route_id == 1).first()
#     # A1 = RoleRoute(r)
#     # role2.area_set.append(A1)
#     # session.flush()
#     # session.commit()
#     # rout = session.query(Role).filter(Role.role_id==2).delete()
#     # # rout = session.query(Route).filter(Route.route_id==1).delete()
#     # session.commit()
#     # rr = session.query(RoleRoute).filter(RoleRoute.id==1).update({RoleRoute.add: 0})
#     # session.commit()
#
