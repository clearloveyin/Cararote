from ..db import db
from sqlalchemy.orm import relationship
import datetime
from app.db.quotations import Quotations


class ProjectType(db.Model):
    __table_args__ = {"schema": "func"}
    __tablename__ = 'project_type'

    id = db.Column(db.Integer, primary_key=True)
    project_type = db.Column(db.String(100))

    projects = relationship("Projects", backref="projectType")

    def __repr__(self):
        return '<Project_Type id:%r, type:%r>' % (self.id, self.project_type)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class ProjectInsideName(db.Model):
    __table_args__ = {"schema": "func"}
    __tablename__ = 'inside_names'

    inside_id = db.Column(db.Integer, primary_key=True)
    inside_name = db.Column(db.String(100))

    projects = relationship("Projects", backref="insideName")

    def __repr__(self):
        return '<InsideName inside_id:%r, inside_name:%r>' % (self.inside_id, self.inside_name)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class ProjectState(db.Model):
    __table_args__ = {"schema": "func"}
    __tablename__ = 'project_state'

    state_id = db.Column(db.Integer, primary_key=True)
    state_name = db.Column(db.String(100))

    projects = relationship("Projects", backref="projectState")

    def __repr__(self):
        return '<StateName state_id:%r, state_name:%r>' % (self.state_id, self.state_name)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class Projects(db.Model):
    __table_args__ = {"schema": "func"}
    __tablename__ = 'projects'

    proj_id = db.Column(db.Integer, primary_key=True)
    inside_name = db.Column(db.Integer, db.ForeignKey('func.inside_names.inside_id'), index=True)
    proj_type = db.Column(db.Integer, db.ForeignKey('func.project_type.id'), index=True)
    commit_user = db.Column(db.Integer, db.ForeignKey('public.users.user_id'), index=True)
    outside_name = db.Column(db.String(100))
    describe = db.Column(db.String(1024))
    commit_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    proj_state = db.Column(db.Integer, db.ForeignKey('func.project_state.state_id'), index=True)

    quotations = relationship("Quotations", backref="projects")
    resourcesinfo = relationship("InputResourceInfo", backref="projects")
    preconditions = relationship("Preconditions", backref="projects")
    options = relationship("Options", backref="projects")

    def __repr__(self):
        return '<Project proj_id:%r, outside_name:%r>' % (self.proj_id, self.outside_name)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            attr = getattr(self, column.name)
            if isinstance(attr, datetime.datetime) or isinstance(attr, datetime.time) or isinstance(attr, datetime.date):
                attr = attr.strftime("%Y-%m-%d %H:%M:%S")
            d[column.name] = attr
        return d


class ProjectObserver(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'project_observer'

    id = db.Column(db.Integer, primary_key=True)
    observer_id = db.Column(db.Integer, db.ForeignKey('public.users.user_id'))
    proj_id = db.Column(db.Integer, db.ForeignKey('func.projects.proj_id'))

    def __repr__(self):
        return '<Observer proj_id:%r, observer_id:%r' % (self.proj_id, self.observer_id)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d
