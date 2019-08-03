# -*- coding: UTF-8 -*-
from flask import current_app
from app.db.users import *
from app.db import db
from app.ctrl.ctrl_base import CtrlBase
from sqlalchemy import or_, and_


class CtrlUser(CtrlBase):
    def __init__(self):
        CtrlBase.__init__(self)

    def register(self, username='', work_id=''):
        if username:
            user = db.session.query(Users).filter(Users.user_name == username).first()
            if user:  # 用户已经存在
                user_id = user.user_id
                user_dict = user.to_dict()
                user_dict['role_list'] = self.get_user_roles(user_id)
                return user_dict
            else:  # 新用户
                user = self.add(username, work_id)
                if user:
                    user_dict = user.to_dict()
                    user_dict['role_list'] = []
                    return user_dict
        return {}

    def add(self, username='', work_id=''):
        if username:
            user = Users(user_name=username, user_type='NORMAL', work_id=work_id)
            db.session.add(user)
            db.session.commit()
            return user
        return None

    def get_user_by_name(self, username):
        q = db.session.query(Users)
        user = q.filter(Users.user_name == username).first()
        if user:
            return user
        return None

    def get_user_by_work(self, work_id):
        q = db.session.query(Users)
        user = q.filter(Users.work_id == work_id).first()
        if user:
            return user
        return None

    def get_one_user(self, user_id):
        q = db.session.query(Users).filter(Users.user_id == user_id).first()
        if q:
            return q.to_dict()
        return None

    def add_user(self, username):
        user = self.get_user_by_name(username)
        if user:
            return user, ""
        else:
            error = "%s还没登录过系统，无法创建该体制！" % username
            # user = Users(user_name=username, user_type='NORMAL', work_id="")  # 测试先加进去
            # db.session.add(user)
            return user, error

    def get_all_user(self):
        user_list = []
        q = db.session.query(Users).order_by(Users.work_id)
        for user in q:
            user_list.append(user.to_dict())
        return user_list

    def out_project_user_roles(self, user_id):
        """取不带项目信息的角色"""
        role_list = []
        q = (db.session.query(Roles)
             .outerjoin(UserRole, Roles.role_id == UserRole.role_id)
             .filter(UserRole.user_id == user_id)
             .filter(UserRole.proj_id.is_(None))
             )
        q = q.distinct()
        for role in q:
            role_list.append(role.role_name)
        return role_list

    def get_user_roles(self, user_id, proj_id=None):
        role_list = []
        q = (db.session.query(Roles)
             .outerjoin(UserRole, Roles.role_id == UserRole.role_id)
             .filter(UserRole.user_id == user_id))
        if proj_id:
            q = q.filter(UserRole.proj_id == proj_id)
        q = q.distinct()
        for role in q:
            role_list.append(role.role_name)
        return role_list

    def extend_user_roles_to_table(self, old_proj_id, proj_id, user_id):
        from app.db.projects import ProjectObserver
        q = (db.session.query(UserRole)
             .filter(UserRole.proj_id == old_proj_id)
             .all())
        q2 = (db.session.query(ProjectObserver)
              .filter(ProjectObserver.proj_id == old_proj_id)
              .all())
        old_observer_list = [ob.observer_id for ob in q2]
        for i in q:
            if i.role_id == 1 and (i.user_id not in old_observer_list):
                info = {
                    UserRole.proj_id.name: proj_id,
                    UserRole.group_id.name: i.group_id,
                    UserRole.role_id.name: i.role_id,
                    UserRole.user_id.name: user_id,
                }
                pro = UserRole(**info)
                db.session.add(pro)
            if i.role_id != 1:
                info = {
                    UserRole.proj_id.name: proj_id,
                    UserRole.group_id.name: i.group_id,
                    UserRole.role_id.name: i.role_id,
                    UserRole.user_id.name: i.user_id,
                }
                pro = UserRole(**info)
                db.session.add(pro)

    def get_out_project_super_pl(self):
        super_pl_list = []
        qs = (db.session.query(Users)
              .outerjoin(UserRole, Users.user_id == UserRole.user_id)
              .outerjoin(Roles, UserRole.role_id == Roles.role_id)
              .filter(Roles.role_name == "SuperPL")
              .filter(UserRole.proj_id.is_(None)))
        for q in qs:
            user = dict()
            user[Users.user_id.name] = q.user_id
            user[Users.user_name.name] = q.user_name
            super_pl_list.append(user)
        return super_pl_list

    def get_out_project_pl(self):
        pl_list = []
        qs = (db.session.query(Users)
              .outerjoin(UserRole, Users.user_id == UserRole.user_id)
              .outerjoin(Roles, UserRole.role_id == Roles.role_id)
              .filter(Roles.role_name == "SALES")
              .filter(UserRole.proj_id.is_(None)))
        for q in qs:
            user = dict()
            user[Users.user_id.name] = q.user_id
            user[Users.user_name.name] = q.user_name
            pl_list.append(user)
        return pl_list

    def get_super_pl_and_pl(self):
        from functools import reduce
        super_pl_list = self.get_out_project_super_pl()
        pl_list = self.get_out_project_pl()
        merge_user_list = super_pl_list+pl_list
        run_function = lambda x, y: x if y in x else x + [y]
        merge_user_list = reduce(run_function, [[], ] + merge_user_list)  # 去重
        for user in merge_user_list:
            if user in super_pl_list:
                super_pl = True
            else:
                super_pl = False
            if user in pl_list:
                pl = True
            else:
                pl = False
            user["super_pl"] = super_pl
            user["pl"] = pl
        if merge_user_list:
            merge_user_list = sorted(merge_user_list, key=lambda k: k['user_name'])  # 排序
        return merge_user_list

    def update_pl_user(self, pl_user_data):
        curr_app = current_app._get_current_object()
        super_pl_role_id = curr_app.config.get("SUPER_PL_ROLE_ID")
        sales_role_id = curr_app.config.get("SALES_ROLE_ID")
        try:
            old_user_role = self.get_pl_user_role(super_pl_role_id, sales_role_id)
            new_user_role = self.get_new_pl_user_role(pl_user_data, old_user_role, super_pl_role_id, sales_role_id)
            self.add_list(UserRole, new_user_role, old_user_role, UserRole.id, [UserRole.role_id.name])
            db.session.commit()
            return True, ""
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"

    def get_new_pl_user_role(self, pl_user_data, old_user_role, super_pl_role_id, sales_role_id):
        user_role_dict = dict()
        for user_role in old_user_role:
            user_id = user_role.get("user_id")
            role_id = user_role.get("role_id")
            user_role_dict[str(user_id) + str(role_id)] = user_role.get("id")
        new_user_role = []
        for pl_user in pl_user_data:
            user_id = pl_user.get("user_id")
            if pl_user.get("super_pl"):
                new_pl = {UserRole.user_id.name: user_id,
                          UserRole.role_id.name: super_pl_role_id,
                          UserRole.proj_id.name: None,
                          UserRole.group_id.name: 1  # 系统默认的pl组
                          }
                if str(user_id) + str(super_pl_role_id) in user_role_dict:
                    new_pl[UserRole.id.name] = user_role_dict.get(str(user_id) + str(super_pl_role_id))
                new_user_role.append(new_pl)
            if pl_user.get("pl"):
                new_pl = {UserRole.user_id.name: user_id,
                          UserRole.role_id.name: sales_role_id,
                          UserRole.proj_id.name: None,
                          UserRole.group_id.name: 1  # 系统默认的pl组
                          }
                if str(user_id) + str(sales_role_id) in user_role_dict:
                    new_pl[UserRole.id.name] = user_role_dict.get(str(user_id) + str(sales_role_id))
                new_user_role.append(new_pl)
        return new_user_role

    def get_pl_user_role(self, super_pl_role_id, sales_role_id):
        user_role_list = []
        qs = (db.session.query(UserRole)
              .filter(UserRole.proj_id.is_(None))
              .filter(UserRole.group_id == 1)
              .filter(UserRole.role_id.in_([super_pl_role_id, sales_role_id])))
        for q in qs:
            user_role_list.append(q.to_dict())
        return user_role_list
