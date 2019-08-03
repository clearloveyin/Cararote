# -*- coding: UTF-8 -*-
from app.db import db


class Car(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'car'

    car_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))  # 车种名称


    def __repr__(self):
        return '<Car %r:%r>' % (self.car_id, self.name)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d

class Destination(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'destination'

    destination_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))  # 仕向地名称


    def __repr__(self):
        return '<Dest %r:%r>' % (self.destination_id, self.name)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d

class Combination(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'combination'

    combination_key = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('public.car.car_id'), index=True)  # 车种ID
    destination_id = db.Column(db.Integer, db.ForeignKey('public.destination.destination_id'), index=True)  # 仕向地ID
    proj_id = db.Column(db.Integer, db.ForeignKey('public.project.proj_id'), index=True)  # 项目ID



    def __repr__(self):
        return '<Combination %r>' % self.combination_key

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d