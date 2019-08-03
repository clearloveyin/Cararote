from ..db import db
import datetime
from sqlalchemy.orm import relationship
from app.db.resources import *


class FileSeq(db.Model):
    __tablename__ = 'file_seq'
    file_id = db.Column(db.Integer, primary_key=True)


class Quotations(db.Model):
    __table_args__ = {"schema": "func"}
    __tablename__ = 'quotations'

    quotation_id = db.Column(db.Integer, primary_key=True)
    parent_quotation_id = db.Column(db.Integer, index=True)
    quotation_ver = db.Column(db.Integer, index=True)
    proj_id = db.Column(db.Integer, db.ForeignKey('func.projects.proj_id'), index=True)
    quotation_name = db.Column(db.String(100))
    base_quotation_id = db.Column(db.Integer, default=0)  # quotation_id, 默认为零
    destribe = db.Column(db.String())
    create_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    create_user = db.Column(db.Integer, db.ForeignKey('public.users.user_id'), index=True)
    update_user = db.Column(db.Integer, db.ForeignKey('public.users.user_id'), index=True)
    status = db.Column(db.String(100), index=True)

    resource_quotation = relationship('ResourceQuotation', backref='quotations')

    def __repr__(self):
        return '<Quotation quotation_id:%r quotation_name:%r>' % (self.quotation_id, self.quotation_name)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            attr = getattr(self, column.name)
            if isinstance(attr, datetime.datetime) or isinstance(attr, datetime.time) or isinstance(attr, datetime.date):
                attr = attr.strftime("%Y-%m-%d %H:%M:%S")
            d[column.name] = attr
        return d


db.Index('func_quotations_proj_id_parent_quotation_id_idx',
         Quotations.proj_id, Quotations.parent_quotation_id,
         )


class FuncStatus(db.Model):
    __table_args__ = {"schema": "func"}
    __tablename__ = 'func_status'

    status_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(100))

    def __repr__(self):
        return '<Funcstatus %r>' % self.status

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class Category(db.Model):
    __table_args__ = {"schema": "func"}
    __tablename__ = 'category'

    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100))

    functions = relationship('Functions', backref='category')

    def __repr__(self):
        return '<Funcstatus %r>' % self.status

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class Functions(db.Model):
    __table_args__ = {"schema": "func"}
    __tablename__ = 'functions'

    func_id = db.Column(db.Integer, primary_key=True)
    base_func_id = db.Column(db.Integer, default=0)  # 继承的func_id, 默认为零
    sub1 = db.Column(db.String(200))
    sub2 = db.Column(db.String(200))
    sub3 = db.Column(db.String(200))
    sub4 = db.Column(db.String(200))
    sub5 = db.Column(db.String(200))
    sub6 = db.Column(db.String(200))
    sub7 = db.Column(db.String(200))
    sub8 = db.Column(db.String(200))
    sub9 = db.Column(db.String(200))
    sub10 = db.Column(db.String(200))
    func_version = db.Column(db.Integer)
    describe = db.Column(db.String(1024))
    update_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    create_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    create_user = db.Column(db.Integer, db.ForeignKey('public.users.user_id'), index=True)
    update_user = db.Column(db.Integer, db.ForeignKey('public.users.user_id'), index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('func.category.category_id'), index=True)
    quotation_id = db.Column(db.Integer, db.ForeignKey('func.quotations.quotation_id'), index=True)
    order_id = db.Column(db.Integer)  # 排序id
    tasks = relationship("Task", backref="function")

    def __repr__(self):
        return '<Function %r>' % self.func_name

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            attr = getattr(self, column.name)
            if isinstance(attr, datetime.datetime) or isinstance(attr, datetime.time) or isinstance(attr, datetime.date):
                attr = attr.strftime("%Y-%m-%d %H:%M:%S")
            d[column.name] = attr
        return d


class Task(db.Model):
    __table_args__ = {"schema": "func"}
    __tablename__ = 'task'

    task_id = db.Column(db.Integer, primary_key=True)
    task1 = db.Column(db.String(200))
    task2 = db.Column(db.String(200))
    task3 = db.Column(db.String(200))
    task4 = db.Column(db.String(200))
    task5 = db.Column(db.String(200))
    task6 = db.Column(db.String(200))
    task_version = db.Column(db.Integer)
    # describe = db.Column(db.String(1024))
    update_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    create_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    create_user = db.Column(db.Integer, db.ForeignKey('public.users.user_id'), index=True)
    update_user = db.Column(db.Integer, db.ForeignKey('public.users.user_id'), index=True)
    func_id = db.Column(db.Integer, db.ForeignKey('func.functions.func_id'), index=True)
    group_id = db.Column(db.Integer, db.ForeignKey('public.group.group_id'), index=True)
    order_id = db.Column(db.Integer)  # 排序id
    delete = db.Column(db.BOOLEAN, default=False)  # 是否是删除的

    def __repr__(self):
        return '<Function %r>' % self.func_name

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            attr = getattr(self, column.name)
            if isinstance(attr, datetime.datetime) or isinstance(attr, datetime.time) or isinstance(attr, datetime.date):
                attr = attr.strftime("%Y-%m-%d %H:%M:%S")
            d[column.name] = attr
        return d


class Options(db.Model):
    __table_args__ = {"schema": "func"}
    __tablename__ = 'options'

    option_id = db.Column(db.Integer, primary_key=True)
    option_name = db.Column(db.String(1024))
    create_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    proj_id = db.Column(db.Integer, db.ForeignKey('func.projects.proj_id'), index=True)
    quotation_id = db.Column(db.Integer, db.ForeignKey('func.quotations.quotation_id'), index=True)

    option_value = relationship("OptionValue", backref="options")
    # func_man_days = relationship("FuncManDay", backref="options")
    # faults = relationship('Fault', backref='options')

    def __repr__(self):
        return '<option %r>' % self.option_name

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            attr = getattr(self, column.name)
            if isinstance(attr, datetime.datetime) or isinstance(attr, datetime.time) or isinstance(attr, datetime.date):
                attr = attr.strftime("%Y-%m-%d %H:%M:%S")
            d[column.name] = attr
        return d


class OptionCombination(db.Model):
    __table_args__ = {"schema": "func"}
    __tablename__ = 'option_combination'

    id = db.Column(db.Integer, primary_key=True)
    quotation_id = db.Column(db.Integer, db.ForeignKey('func.quotations.quotation_id'), index=True)
    option_value_id_list = db.Column(db.String(1024))
    value = db.Column(db.String(1024))
    proj_id = db.Column(db.Integer, db.ForeignKey('func.projects.proj_id'), index=True)
    checked = db.Column(db.Boolean, index=True)

    func_man_days = relationship("FuncManDay", backref="option_combination")

    def __repr__(self):
        return '<Combination %r>' % self.value

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            attr = getattr(self, column.name)
            if isinstance(attr, datetime.datetime) or isinstance(attr, datetime.time) or isinstance(attr, datetime.date):
                attr = attr.strftime("%Y-%m-%d %H:%M:%S")
            d[column.name] = attr
        return d


class OptionValue(db.Model):
    __table_args__ = {"schema": "func"}
    __tablename__ = 'option_value'

    value_id = db.Column(db.Integer, primary_key=True)
    option_id = db.Column(db.Integer, db.ForeignKey('func.options.option_id'), index=True)
    option_value = db.Column(db.String(1024))

    def __repr__(self):
        return '<OptionValue %r>' % self.option_value

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            attr = getattr(self, column.name)
            if isinstance(attr, datetime.datetime) or isinstance(attr, datetime.time) or isinstance(attr, datetime.date):
                attr = attr.strftime("%Y-%m-%d %H:%M:%S")
            d[column.name] = attr
        return d


class Preconditions(db.Model):
    __table_args__ = {"schema": "func"}
    __tablename__ = 'preconditions'

    pre_id = db.Column(db.Integer, primary_key=True)
    precondition = db.Column(db.String(4096))
    # create_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    # update_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    proj_id = db.Column(db.Integer, db.ForeignKey('func.projects.proj_id'), index=True)
    quotation_id = db.Column(db.Integer, db.ForeignKey('func.quotations.quotation_id'), index=True)

    func_man_days = relationship("FuncManDay", backref="precondition")

    def __repr__(self):
        return '<precondition %r>' % self.precondition

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            attr = getattr(self, column.name)
            if isinstance(attr, datetime.datetime) or isinstance(attr, datetime.time) or isinstance(attr, datetime.date):
                attr = attr.strftime("%Y-%m-%d %H:%M:%S")
            d[column.name] = attr
        return d


class FuncManDay(db.Model):
    __table_args__ = {"schema": "func"}
    __tablename__ = 'func_man_day'

    id = db.Column(db.Integer, primary_key=True)
    base_id = db.Column(db.Integer)
    task_id = db.Column(db.Integer, db.ForeignKey('func.task.task_id'))
    group_id = db.Column(db.Integer, db.ForeignKey('public.group.group_id'))
    option_id = db.Column(db.Integer, db.ForeignKey('func.option_combination.id'))
    pre_id = db.Column(db.Integer, db.ForeignKey('func.preconditions.pre_id'))
    assin_to = db.Column(db.Integer, db.ForeignKey('public.users.user_id'))
    status_id = db.Column(db.Integer, db.ForeignKey('func.func_status.status_id'))
    days = db.Column(db.Float)
    comment = db.Column(db.String(4096))
    version = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    create_user = db.Column(db.Integer, db.ForeignKey('public.users.user_id'))
    update_user = db.Column(db.Integer, db.ForeignKey('public.users.user_id'))

    def __repr__(self):
        return '<id %r, task_id %r>' % self.id, self.task_id

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            attr = getattr(self, column.name)
            if isinstance(attr, datetime.datetime) or isinstance(attr, datetime.time) or isinstance(attr, datetime.date):
                attr = attr.strftime("%Y-%m-%d %H:%M:%S")
            d[column.name] = attr
        return d


db.Index('func_func_man_day_task_option_group_version_id_idx',
         FuncManDay.task_id, FuncManDay.group_id,
         FuncManDay.option_id, FuncManDay.version,
         unique=True
         )


class FuncGroup(db.Model):
    __table_args__ = {"schema": "func"}
    __tablename__ = 'func_group'

    id = db.Column(db.Integer, primary_key=True)
    func_id = db.Column(db.Integer, db.ForeignKey('func.functions.func_id'), index=True)
    group_id = db.Column(db.Integer, db.ForeignKey('public.group.group_id'), index=True)
    group_role = db.Column(db.String(100))  # major:主担当组/minor:关联组


db.Index('func_func_group_func_id_group_id_idx',
         FuncGroup.func_id, FuncGroup.group_id,
         unique=True
         )
