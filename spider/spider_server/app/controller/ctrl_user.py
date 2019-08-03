from app.db import db
from app.db.user import Users, Role


class CtrlUser(object):
    def __init__(self):
        self.user_model = Users

    def get_all_users(self):
        user_list = []
        qs = (db.session.query(Users.user_id, Users.user_name)
              .filter(Users.user_name != "Admin")
              .order_by(Users.user_name))
        for q in qs:
            user_dict = dict()
            user_dict[Users.user_id.name] = q.user_id
            user_dict[Users.user_name.name] = q.user_name
            user_list.append(user_dict)
        return user_list

    def get_all_roles(self):
        role_list = []
        qs = db.session.query(Role).filter(Role.type == "Project")
        for q in qs:
            role_list.append(q.to_dict())
        return role_list

    def get_user_by_name(self, username):
        q = db.session.query(Users)
        user = q.filter(Users.user_name == username).first()
        if user:
            return user
        return None

    def add_new_user(self, user_name):
        q = db.session.query(Users).filter(Users.user_name == user_name).first()
        if not q:
            user = Users(**{Users.user_name.name: user_name})
            db.session.add(user)
            db.session.flush()
            return user.to_dict()
        else:
            return q.to_dict()

    def register(self, username='', work_id=''):
        user = db.session.query(Users).filter(Users.user_emp_id == work_id).first()
        if user:  # 用户已经存在
            user_dict = user.to_dict()
            return user_dict
        else:  # 新用户
            user = self.add(username, work_id)
            if user:
                user_dict = user.to_dict()
                return user_dict

    def add(self, username='', work_id=''):
        if username:
            user = Users(user_name=username, user_emp_id=work_id)
            db.session.add(user)
            db.session.commit()
            return user
        return None