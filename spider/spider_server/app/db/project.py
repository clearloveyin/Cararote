# -*- coding: UTF-8 -*-
from app.db import db
import datetime
from sqlalchemy.orm import relationship


class Project(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'project'

    proj_id = db.Column(db.Integer, primary_key=True)
    proj_name = db.Column(db.String(256), index=True)  # 项目标题
    describe = db.Column(db.String())  # 概述
    create_user = db.Column(db.Integer, db.ForeignKey('public.users.user_id'), index=True)  # 创建人
    update_user = db.Column(db.Integer, db.ForeignKey('public.users.user_id'), index=True)  # 更新人
    status = db.Column(db.String(256), index=True)  # 状态
    create_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)  # 创建时间
    update_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)  # 更新时间


    def __repr__(self):
        return '<Project %r:%r>' % (self.proj_id, self.proj_name)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            attr = getattr(self, column.name)
            if isinstance(attr, datetime.datetime) or isinstance(attr, datetime.time) or isinstance(attr, datetime.date):
                attr = attr.strftime("%Y-%m-%d %H:%M:%S")
            d[column.name] = attr
        return d

class ProjectRoles(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'project_roles'

    gid = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('public.users.user_id'), index=True)  # 用户id
    role_id = db.Column(db.Integer, db.ForeignKey('public.role.role_id'), index=True)  # 角色id
    proj_id = db.Column(db.Integer, db.ForeignKey('public.project.proj_id'), index=True)  # 项目id

    def __repr__(self):
        return '<UserRoles %r:%r>' % (self.user_id, self.role_id)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d

class ProjFunc(db.Model):
    __table_args__ = (
        db.ForeignKeyConstraint(
            ["func_id", "ver"],
            ["func.spec_func.func_id", "func.spec_func.ver"],
            name="proj_func"
        ),
        {"schema": "func"}
    )
    __tablename__ = 'proj_func'

    id = db.Column(db.Integer, primary_key=True)
    proj_id = db.Column(db.Integer, db.ForeignKey('public.project.proj_id'), index=True)  # 项目id
    func_id = db.Column(db.Integer)
    ver = db.Column(db.Integer)
    db.ForeignKeyConstraint(['func_id', 'ver'], ['func.spec_func.func_id', 'func.spec_func.ver'])
    status = db.Column(db.String(256), index=True)  # 状态
    create_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)  # 创建时间
    feature_change_status = db.Column(db.Integer)  # feature变更ID
    expend_id = db.Column(db.Integer)  # 展开ID
    apply_expend = db.Column(db.Boolean)  # 是否展开


    def __repr__(self):
        return '<ProjFunc %r:%r>' % (self.func_id, self.ver)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            attr = getattr(self, column.name)
            if isinstance(attr, datetime.datetime) or isinstance(attr, datetime.time) or isinstance(attr, datetime.date):
                attr = attr.strftime("%Y-%m-%d %H:%M:%S")
            d[column.name] = attr
        return d

db.Index('func_proj_func_func_id_ver_idx',
         ProjFunc.func_id, ProjFunc.ver,
         unique=True
         )

class ProjCatalog(db.Model):
    __table_args__ = (
        db.ForeignKeyConstraint(
            ["catalog_id", "ver"],
            ["func.spec_catalog.catalog_id", "func.spec_catalog.ver"],
            name="proj_catalog"
        ),
        {"schema": "func"}
    )
    __tablename__ = 'proj_catalog'

    id = db.Column(db.Integer, primary_key=True)
    proj_id = db.Column(db.Integer, db.ForeignKey('public.project.proj_id'), index=True)  # 项目id
    catalog_id = db.Column(db.Integer)
    ver = db.Column(db.Integer)
    status = db.Column(db.String(256), index=True)
    create_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)  # 创建时间
    expend_id = db.Column(db.Integer)  # 展开ID

    def __repr__(self):
        return '<ProjCatalog %r:%r>' % (self.catalog_id, self.ver)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            attr = getattr(self, column.name)
            if isinstance(attr, datetime.datetime) or isinstance(attr, datetime.time) or isinstance(attr, datetime.date):
                attr = attr.strftime("%Y-%m-%d %H:%M:%S")
            d[column.name] = attr
        return d

class ProjFeature(db.Model):
    __table_args__ = (
        db.ForeignKeyConstraint(
            ["feature_id", "ver"],
            ["func.feature.feature_id", "func.feature.ver"],
            name="proj_feature"
        ),
        {"schema": "func"}
    )
    __tablename__ = 'proj_feature'

    proj_feature_key = db.Column(db.Integer, primary_key=True)
    proj_id = db.Column(db.Integer, db.ForeignKey('public.project.proj_id'), index=True)  # 项目id
    feature_id = db.Column(db.Integer)
    ver = db.Column(db.Integer)
    statement = db.Column(db.String(1024))
    remark = db.Column(db.String(1024))
    qa = db.Column(db.String())
    spec_change = db.Column(db.String(256))
    creat_user = db.Column(db.Integer, db.ForeignKey('public.users.user_id'), index=True)
    update_user = db.Column(db.Integer, db.ForeignKey('public.users.user_id'), index=True)
    creat_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    status = db.Column(db.String(256), index=True)
    apply_expend = db.Column(db.Boolean)
    expend_id = db.Column(db.Integer)

    def __repr__(self):
        return '<ProjFeature %r:%r>' % (self.user_id, self.role_id)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            attr = getattr(self, column.name)
            if isinstance(attr, datetime.datetime) or isinstance(attr, datetime.time) or isinstance(attr, datetime.date):
                attr = attr.strftime("%Y-%m-%d %H:%M:%S")
            d[column.name] = attr
        return d

class ProjFeatureCombination(db.Model):
    __table_args__ = {"schema": "func"}
    __tablename__ = 'proj_feature_combination'

    id = db.Column(db.Integer, primary_key=True)
    proj_feature_key = db.Column(db.Integer, db.ForeignKey('func.proj_feature.proj_feature_key'))  # proj_feature
    combination_id = db.Column(db.Integer, db.ForeignKey('public.combination.combination_key'))  # 车种仕向地组合key
    content = db.Column(db.String(1024))

    def __repr__(self):
        return '<UserRoles %r:%r>' % (self.user_id, self.role_id)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d