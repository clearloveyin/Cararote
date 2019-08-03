# -*- coding: UTF-8 -*-
from app.db import db
import datetime


class CommonKey(db.Model):
    __table_args__ = {"schema": "func"}
    __tablename__ = 'common_key'

    key_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100))  # func,catalog,feature


    def __repr__(self):
        return '<CommonKey %r:%r>' % (self.common_key, self.type)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d

class SpecFunc(db.Model):
    __table_args__ = (
        db.UniqueConstraint("func_id", "ver"),
        {"schema": "func"}
    )
    __tablename__ = 'spec_func'

    func_key = db.Column(db.Integer, primary_key=True)
    func_id = db.Column(db.Integer, db.ForeignKey('func.common_key.key_id'))  # ID
    func_no = db.Column(db.String())  # 项目ID
    func_title = db.Column(db.String(256))  # func,catalog,feature
    func_type = db.Column(db.String(100))  # func,catalog,feature
    content = db.Column(db.String())  # func,catalog,feature
    parent_func_id = db.Column(db.Integer)
    ver = db.Column(db.Integer)  # func,catalog,feature
    catalog_id = db.Column(db.Integer)  # func,catalog,feature
    test_type = db.Column(db.String(100))  # func,catalog,feature
    create_user = db.Column(db.Integer, db.ForeignKey('public.users.user_id'), index=True)  # func,catalog,feature
    update_user = db.Column(db.Integer, db.ForeignKey('public.users.user_id'), index=True)  # func,catalog,feature
    create_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)  # func,catalog,feature
    status = db.Column(db.String(100), index=True)  # func,catalog,feature


    def __repr__(self):
        return '<SpecFunc key:%r func_id:%r>' % (self.func_key, self.func_id)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            attr = getattr(self, column.name)
            if isinstance(attr, datetime.datetime) or isinstance(attr, datetime.time) or isinstance(attr, datetime.date):
                attr = attr.strftime("%Y-%m-%d %H:%M:%S")
            d[column.name] = attr
        return d

class SpecCatalog(db.Model):
    __table_args__ = (
        db.UniqueConstraint("catalog_id", "ver"),
        {"schema": "func"}
    )
    __tablename__ = 'spec_catalog'

    catalog_key = db.Column(db.Integer, primary_key=True)
    catalog_id = db.Column(db.Integer, db.ForeignKey('func.common_key.key_id'), index=True)  # ID
    catalog_no = db.Column(db.String())  # 项目ID
    catalog_title = db.Column(db.String(256))  # func,catalog,feature
    type = db.Column(db.String(256))  # func,catalog,feature
    outline = db.Column(db.String())  # func,catalog,feature
    precondition = db.Column(db.String())  # func,catalog,feature
    invocation = db.Column(db.String())  # func,catalog,feature
    parent_cat_id = db.Column(db.Integer, nullable=False, default=0)
    ver = db.Column(db.Integer)  #
    create_user = db.Column(db.Integer, db.ForeignKey('public.users.user_id'), index=True)  # func,catalog,feature
    update_user = db.Column(db.Integer, db.ForeignKey('public.users.user_id'), index=True)  # func,catalog,feature
    create_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)  # func,catalog,feature

    def __repr__(self):
        return '<SpecCatalog key:%r catalog_id:%r>' % (self.catalog_key, self.catalog_id)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            attr = getattr(self, column.name)
            if isinstance(attr, datetime.datetime) or isinstance(attr, datetime.time) or isinstance(attr, datetime.date):
                attr = attr.strftime("%Y-%m-%d %H:%M:%S")
            d[column.name] = attr
        return d

class Feature(db.Model):
    __table_args__ = (
        db.UniqueConstraint("feature_id", "ver"),
        {"schema": "func"}
    )
    __tablename__ = 'feature'

    feature_key = db.Column(db.Integer, primary_key=True)
    feature_id = db.Column(db.Integer, db.ForeignKey('func.common_key.key_id'))  # ID
    feature_no = db.Column(db.String())  # 项目ID
    feature_name = db.Column(db.String(256))  # func,catalog,feature
    feature_type = db.Column(db.String(256))  # func,catalog,feature
    parent_feature_id = db.Column(db.Integer)
    ver = db.Column(db.Integer)  # feature 版本
    status = db.Column(db.String(256), index=True)  # func,catalog,feature
    reason_details = db.Column(db.String(1024))  # func,catalog,feature
    version = db.Column(db.String())  # 变更理由版本
    create_user = db.Column(db.Integer, db.ForeignKey('public.users.user_id'), index=True)  # func,catalog,feature
    update_user = db.Column(db.Integer, db.ForeignKey('public.users.user_id'), index=True)  # func,catalog,feature
    create_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)  # func,catalog,feature
    update_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    update_type = db.Column(db.String())

    def __repr__(self):
        return '<Feature key:%r catalog_id:%r>' % (self.feature_key, self.feature_id)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            attr = getattr(self, column.name)
            if isinstance(attr, datetime.datetime) or isinstance(attr, datetime.time) or isinstance(attr, datetime.date):
                attr = attr.strftime("%Y-%m-%d %H:%M:%S")
            d[column.name] = attr
        return d

class RFQ(db.Model):
    __table_args__ = {"schema": "func"}
    __tablename__ = 'rfq'

    rfq_id = db.Column(db.Integer, primary_key=True)
    proj_id = db.Column(db.Integer, db.ForeignKey('public.project.proj_id'), index=True)  # 项目ID
    comment = db.Column(db.String())

    def __repr__(self):
        return '<RFQ %r>' % self.rfq_id

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            attr = getattr(self, column.name)
            if isinstance(attr, datetime.datetime) or isinstance(attr, datetime.time) or isinstance(attr, datetime.date):
                attr = attr.strftime("%Y-%m-%d %H:%M:%S")
            d[column.name] = attr
        return d

class FeatureRfq(db.Model):
    __table_args__ = {"schema": "func"}
    __tablename__ = 'feature_rfq'

    id = db.Column(db.Integer, primary_key=True)
    proj_feature_key = db.Column(db.Integer, db.ForeignKey('func.proj_feature.proj_feature_key'), index=True)  # proj_feature
    rfq_if = db.Column(db.Integer, db.ForeignKey('func.rfq.rfq_id'), index=True)  # rfq
    description = db.Column(db.String())

    def __repr__(self):
        return '<FeatureRfq %r>' % self.id

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            attr = getattr(self, column.name)
            if isinstance(attr, datetime.datetime) or isinstance(attr, datetime.time) or isinstance(attr, datetime.date):
                attr = attr.strftime("%Y-%m-%d %H:%M:%S")
            d[column.name] = attr
        return d

class FeatureFunc(db.Model):
    __table_args__ = {"schema": "func"}
    __tablename__ = 'feature_func'

    id = db.Column(db.Integer, primary_key=True)
    feature_id = db.Column(db.Integer, db.ForeignKey('func.common_key.key_id'), index=True)  #
    func_id = db.Column(db.Integer, db.ForeignKey('func.common_key.key_id'), index=True)  #
    proj_id = db.Column(db.Integer, db.ForeignKey('public.project.proj_id'), index=True)  # 项目ID



    def __repr__(self):
        return '<FeatureFunc %r>' % self.id

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d
