from ..db import db
import datetime
from sqlalchemy.orm import relationship


class Issue(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'issue'

    issue_id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String())
    status = db.Column(db.String(100))
    commit_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    issue_user = db.Column(db.Integer, db.ForeignKey('public.users.user_id'))
    table_name = db.Column(db.String(100))
    key_id = db.Column(db.Integer)
    col_value = db.Column(db.String())

    replays = relationship('Replay', backref='issue')

    def __repr__(self):
        return '<issue comment:%r>' % self.comment

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class Replay(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'replay'

    replay_id = db.Column(db.Integer, primary_key=True)
    issue_id = db.Column(db.Integer, db.ForeignKey('public.issue.issue_id'))
    parent_replay_id = db.Column(db.Integer, default=0)
    comment = db.Column(db.String())
    status = db.Column(db.String(100))
    commit_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    issue_user = db.Column(db.Integer, db.ForeignKey('public.users.user_id'))
    table_name = db.Column(db.String(100))
    key_id = db.Column(db.Integer)
    col_value = db.Column(db.String())

    def __repr__(self):
        return '<replay comment:%r>' % self.comment

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            attr = getattr(self, column.name)
            if isinstance(attr, datetime.datetime) or isinstance(attr, datetime.time) or isinstance(attr, datetime.date):
                attr = attr.strftime("%Y-%m-%d %H:%M:%S")
            d[column.name] = attr
        return d