from ..db import db
from sqlalchemy.orm import relationship
import datetime


class Users(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    user_emp_id = db.Column(db.String(100))  # 员工号
    user_name = db.Column(db.String(100), index=True)
    email = db.Column(db.String(100))

    def __repr__(self):
        return '<User %r>' % self.username

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class Permission(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'permission'

    perm_id = db.Column(db.Integer, primary_key=True)
    perm_name = db.Column(db.String(100))  # 权限名称
    type = db.Column(db.String(100))  # 类别

    def __repr__(self):
        return '<Permission %r-->%r>' % (self.module_name, self.perm_name)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d

class Role(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'role'

    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(256))
    type = db.Column(db.String(256))

    def __repr__(self):
        return '<Role %r>' % self.role_name

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d

class RolePermission(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'role_perm_rel'

    gid = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('public.role.role_id'))  # 角色id
    perm_id = db.Column(db.Integer, db.ForeignKey('public.permission.perm_id'))  # 权限id

    def __repr__(self):
        return '<RolePermission %r:%r>' % (self.role_id, self.perm_id)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d

