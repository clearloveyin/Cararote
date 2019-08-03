from flask import Flask
from config import config
from app.db import db
from app.db.projects import ProjectInsideName, ProjectState
from app.db.quotations import FuncStatus
from app.db.users import Roles, Group
app = Flask(__name__)
app.config.from_object(config['default'])
db.app = app
db.init_app(app)
inside_name_list = ["shanks", "beckman", "Roux", "yasopp", "Charlotte", "Perospero",
                    "Katakuri", "Cracker", "Snack", "Smoothie", "Tamago",
                    "Pekoms", "Kaido", "JACK", "Holdem", "Speed", "XDrake",
                    "Apoo", "Teech", "Burgess", "Shiryu", "Lafitte", "VanAugur",
                    "DocQ", "SanJuan", "Mihawk", "Doflamingo", "Crocodile",
                    "Moria", "Hancock", "Jimbei", "Bartholomew", "Trafalgar",
                    "Buggy", "Weevil", "Sakazuki", "Kuzan", "Kprusoian", "Zephyr",
                    "Issho", "Sengoku", "Garp", "Tsuru", "Smoker", "Dragon", "Sabo",
                    "Ivankov", "Inazuma", "Koala", "Morley", "Hack", "Roux2"]
for inside_name in inside_name_list:
    project_inside_model = ProjectInsideName(inside_name=inside_name)
    db.session.add(project_inside_model)
project_status_model = ProjectState(state_id=1, state_name="新建")
db.session.add(project_status_model)
project_status_model = ProjectState(state_id=2, state_name="立项")
db.session.add(project_status_model)
project_status_model = ProjectState(state_id=3, state_name="关闭")
db.session.add(project_status_model)
func_status_model = FuncStatus(status_id=1, status="新建")
db.session.add(func_status_model)
func_status_model = FuncStatus(status_id=2, status="处理中")
db.session.add(func_status_model)
func_status_model = FuncStatus(status_id=3, status="确认中")
db.session.add(func_status_model)
func_status_model = FuncStatus(status_id=4, status="已提出")
db.session.add(func_status_model)
func_status_model = FuncStatus(status_id=5, status="已承认")
db.session.add(func_status_model)
role_model = Roles(role_id=1, role_name="SALES")
db.session.add(role_model)
role_model = Roles(role_id=2, role_name="SGL")
db.session.add(role_model)
role_model = Roles(role_id=3, role_name="GL")
db.session.add(role_model)
role_model = Roles(role_id=4, role_name="SuperPL")
db.session.add(role_model)
pl_group_model = Group(group_id=1, group_name="PL", parent_group_id=0)
db.session.add(pl_group_model)
db.session.commit()


