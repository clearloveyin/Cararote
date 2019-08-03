from ..db import db
import datetime
from sqlalchemy.orm import relationship


# class ResourceCat(db.Model):
#     __table_args__ = {"schema": "resource"}
#     __tablename__ = 'resource_cat'
#
#     rsc_cat_id = db.Column(db.Integer, primary_key=True)
#     rsc_cat_name = db.Column(db.String(100))
#
#     def __repr__(self):
#         return '<ReCat rsc_cat_id:%r, rsc_cat_name:%r >' % (self.rsc_cat_id, self.rsc_cat_name)
#
#     def to_dict(self):
#         d = {}
#         for column in self.__table__.columns:
#             d[column.name] = getattr(self, column.name)
#         return d


class InputResourceInfo(db.Model):
    __table_args__ = {"schema": "resource"}
    __tablename__ = 'input_resource_info'

    resource_id = db.Column(db.Integer, primary_key=True)
    commit_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    file_name = db.Column(db.String(100))
    resource_type = db.Column(db.String(100), nullable=False)
    update_user_id = db.Column(db.Integer, db.ForeignKey('public.users.user_id'))
    proj_id = db.Column(db.Integer, db.ForeignKey('func.projects.proj_id'))
    status = db.Column(db.String(10))

    input_resource_data = relationship('InputResourceData', backref='resourceInfo')

    def __repr__(self):
        return '<ReInfo resource_id:%r, rsc_cat_id:%r >' % (self.resource_id, self.rsc_cat_id)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            attr = getattr(self, column.name)
            if isinstance(attr, datetime.datetime) or isinstance(attr, datetime.time) or isinstance(attr, datetime.date):
                attr = attr.strftime("%Y-%m-%d %H:%M:%S")
            d[column.name] = attr
        return d


class InputResourceData(db.Model):
    __table_args__ = {"schema": "resource"}
    __tablename__ = 'input_resource_data'

    id = db.Column(db.Integer, primary_key=True)
    version_id = db.Column(db.String(10))
    url = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('public.users.user_id'))
    commit_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.input_resource_info.resource_id'))
    status = db.Column(db.String(10), nullable=False)

    resource_quotation = relationship('ResourceQuotation', backref='resource_data')

    def __repr__(self):
        return '<ReData id:%r, ver_id:%r >' % (self.id, self.version_id)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            attr = getattr(self, column.name)
            if isinstance(attr, datetime.datetime) or isinstance(attr, datetime.time) or isinstance(attr, datetime.date):
                attr = attr.strftime("%Y-%m-%d %H:%M:%S")
            d[column.name] = attr
        return d


class ResourceQuotation(db.Model):
    __table_args__ = {"schema": "resource"}
    __tablename__ = 'resource_quotation'

    id = db.Column(db.Integer, primary_key=True)
    resource_ver_id = db.Column(db.Integer, db.ForeignKey('resource.input_resource_data.id'))
    quotation_id = db.Column(db.Integer, db.ForeignKey('func.quotations.quotation_id'))

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d






