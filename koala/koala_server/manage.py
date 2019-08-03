# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_script import Manager
# from flask_migrate import Migrate, MigrateCommand
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pset123456@192.168.37.143/test_hcz'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#
# db = SQLAlchemy(app)
# # db.create_all()
# migrate = Migrate(app, db)
#
# manager = Manager(app)
# manager.add_command('db', MigrateCommand)
#
#
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(128))
#
#
# class Test1(db.Model):
#     __table_args__ = {"schema": "ds"}
#     __table_name__ = 'test1'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(128))
#
#
# if __name__ == '__main__':
#     manager.run()
#
from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from config import config
from app.db import db

app = Flask(__name__)
app.config.from_object(config['default'])
# cache.init_app(app)
db.app = app
db.init_app(app)
# from app.db import *
# import app.db
# db.create_all(app=app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


from app.db.users import *
from app.db.projects import *
from app.db.resources import *
from app.db.quotations import *
from app.db.issues import *
from app.db.journal import *


if __name__ == '__main__':
    manager.run()
