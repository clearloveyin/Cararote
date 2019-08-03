# -*- coding: UTF-8 -*-
import copy
import pandas as pd
import os
from flask import current_app
from app.db import db
from sqlalchemy import or_, and_
from app.ctrl.ctrl_base import CtrlBase
from app.ctrl.ctrl_user import CtrlUser
from app.ctrl.ctrl_user_group import CtrlUserGroup
from app.import_file.import_manager import ImportManager
from app.db.projects import *
from app.db.users import Group, Users
from app.ctrl.utility import Utillity
from app.db.users import UserRole
from app.data_server.ds_pieces import refresh_group_df


class CtrlProject(CtrlBase):

    def __init__(self):
        CtrlBase.__init__(self)
        self.key_col = Projects.proj_id
        self.db_object = Projects
        self.col_list = [Projects.inside_name.name, Projects.outside_name.name, Projects.proj_id.name]
        self.del_manday = """
            delete from func.func_man_day where task_id in (
                select task_id from func.task as t1 left join 
                func.functions as t2 on t1.func_id = t2.func_id
                left join func.quotations as t3 
                on t2.quotation_id = t3.quotation_id
                where t3.proj_id = {}
            )
            """
        self.del_task = """
            delete from func.task where func_id in(
                select func_id from func.functions as t1
                left join func.quotations as t2
                on t1.quotation_id = t2.quotation_id
                where t2.proj_id = {}
            )
            """
        self.del_function_one = """
            delete from func.func_group where func_id in(
                select func_id from func.functions as t1
                left join func.quotations as t2
                on t1.quotation_id = t2.quotation_id
                where t2.proj_id = {}
            )
            """
        self.del_function_two = """
            delete from func.functions where quotation_id in(
                select quotation_id from func.quotations 
                where func.quotations.proj_id = {}
            )
            """
        self.del_option_combination = """
            delete from func.option_combination where quotation_id in (
                select quotation_id from func.quotations
                where func.quotations.proj_id = {}
            )
            """
        self.del_option_value = """
            delete from func.option_value where option_id in (
                select option_id from func.options as t1 left join
                func.quotations as t2 on t1.quotation_id = t2.quotation_id 
                where t1.proj_id = {}
            )
            """
        self.del_options = """
            delete from func.options where quotation_id in (
                select quotation_id from func.quotations
                where func.quotations.proj_id = {}
            )
            """
        self.del_preconditions = """
            delete from func.preconditions where func.preconditions.proj_id = {}
            """
        self.del_quotations = """
            delete from func.quotations where func.quotations.proj_id = {}
            """
        self.del_user_role = """
            delete from user_role where user_role.proj_id = {}
            """
        self.del_project_observer = """
            delete from public.project_observer where public.project_observer.proj_id = {}
            """
        self.del_projects = """
            delete from func.projects where func.projects.proj_id = {}
            """

    def add_project_with_observer(self, data):
        try:
            proj_type = data.get('proj_type')
            inside_name = data.get('inside_name')
            commit_user = data.get('commit_user')
            describe = data.get('describe')
            outside_name = data.get('outside_name')
            observer_list = data.get('observer_list')
            role_names = CtrlUser().out_project_user_roles(commit_user)
            if "SALES" not in role_names and "SuperPL" not in role_names:
                return False, "该用户无法创建项目！"
            if not data.get('file_url'):
                if not data.get('manage_id'):
                    return False, "体制表不能为空"
                else:
                    manage_id = int(data.get('manage_id'))
                    file_url = None
            else:
                file_url = data.get("file_url")
                manage_id = None
            if not proj_type:
                return False, "项目系列不能为空"
            if not inside_name:
                return False, "项目内部名称不能为空"
            if not describe:
                return False, "项目详细不能为空"
            if not outside_name:
                return False, "项目客户名称不能为空"
            if not commit_user:
                return False, "提交人不能为空"
            inside_id = self.get_or_add_project_inside_name(inside_name)
            if not inside_id:
                return False, "此内部名称已被使用"
            proj_type_id = self.get_or_add_project_type(proj_type)
            proj_id = self.add_proj_to_table(inside_id, outside_name, proj_type_id, describe, commit_user)
            oblist = set([observer.get("value") for observer in observer_list])
            for observer in oblist:
                if observer and (observer != commit_user):
                    self.add_observer(observer, proj_id)
            if file_url:
                res, msg = self.import_project_manager(file_url, proj_id)
                if not res:
                    return False, msg
            else:
                CtrlUser().extend_user_roles_to_table(manage_id, proj_id, commit_user)
            db.session.commit()
            refresh_group_df()
            return proj_id, ""
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"

    def get_or_add_project_type(self, proj_type):
        proj_type_obj = (db.session.query(ProjectType)
                         .filter(ProjectType.project_type == proj_type)
                         .first())
        if proj_type_obj:
            proj_type_id = proj_type_obj.id
        else:
            proj_type_id = self.add_proj_type(proj_type)
        return proj_type_id

    def get_or_add_project_inside_name(self, inside_name):
        inside_name_obj = (db.session.query(ProjectInsideName)
                           .filter(ProjectInsideName.inside_name == inside_name)
                           .first())
        if inside_name_obj:
            q = db.session.query(Projects).filter(Projects.inside_name == inside_name_obj.inside_id).first()
            if q:
                return False
            else:
                return inside_name_obj.inside_id
        else:
            inside_id = self.add_proj_inside_name(inside_name)
            return inside_id

    def add_observer(self, observer, proj_id):
        observer_info = {
            ProjectObserver.proj_id.name: proj_id,
            ProjectObserver.observer_id.name: observer,
        }
        role = (db.session.query(UserRole)
                .filter(UserRole.user_id == observer)
                .filter(UserRole.role_id == 1)
                .filter(UserRole.proj_id == proj_id)
                .filter(UserRole.group_id == 1).first())
        if not role:
            user_role_info = {
                UserRole.user_id.name: observer,
                UserRole.proj_id.name: proj_id,
                UserRole.role_id.name: 1,
                UserRole.group_id.name: 1,
            }
            role = UserRole(**user_role_info)
            db.session.add(role)
        pro = ProjectObserver(**observer_info)
        db.session.add(pro)

    def add_proj_inside_name(self, value):
        q = db.session.query(ProjectInsideName).filter(ProjectInsideName.inside_name == value).first()
        if q:
            return False
        name_info = {
            ProjectInsideName.inside_name.name: value,
        }
        name = ProjectInsideName(**name_info)
        db.session.add(name)
        db.session.flush()
        return name.inside_id

    def add_proj_type(self, value):
        q = db.session.query(ProjectType).filter(ProjectType.project_type == value).first()
        if q:
            return q.id
        type_info = {
            ProjectType.project_type.name: value,
        }
        proj_type = ProjectType(**type_info)
        db.session.add(proj_type)
        db.session.flush()
        return proj_type.id

    def add_proj_to_table(self, inside_id, outside_name, proj_type_id, describe, commit_user):
        pro_info = {
            Projects.inside_name.name: inside_id,
            Projects.outside_name.name: outside_name,
            Projects.proj_type.name: proj_type_id,
            Projects.describe.name: describe,
            Projects.commit_time.name: self.get_current_time(),
            Projects.update_time.name: self.get_current_time(),
            Projects.proj_state.name: 1,                 # 新建
            Projects.commit_user.name: commit_user,
        }
        pro = Projects(**pro_info)
        db.session.add(pro)
        db.session.flush()
        return pro.proj_id

    def get_inside_name_list(self):
        name_list = []
        q = db.session.query(ProjectInsideName).order_by(ProjectInsideName.inside_id).all()
        for name in q:
            name_list.append({"inside_id": name.inside_id, "inside_name": name.inside_name})
        return name_list

    def get_proj_type_list(self):
        type_list = []
        q = db.session.query(ProjectType).order_by(ProjectType.id).all()
        for name in q:
            type_list.append({"type_id": name.id, "proj_type": name.project_type})
        return type_list

    def check_proj_name(self):
        """
        将已经存在引用的InsideName返回给前端
        :return:
        """
        type_list = []
        q = (db.session.query(Projects.inside_name, ProjectInsideName.inside_name)
             .outerjoin(ProjectInsideName, Projects.inside_name == ProjectInsideName.inside_id)
             .order_by(Projects.inside_name).all())
        for name in q:
            type_list.append({"inside_id": name[0], "inside_name": name[1]})
        return type_list

    def get_proj_state_options(self):
        name_list = []
        q = db.session.query(ProjectState).order_by(ProjectState.state_id).all()
        for name in q:
            name_list.append({"state_id": name.state_id, "state_name": name.state_name})
        return name_list

    def get_proj_list(self):
        """
        获取所有的项目
        :param project_type:
        :return:
        """
        project_list = []
        q = (db.session.query(Projects)
             .filter(Projects.proj_state != 3)
             .order_by(Projects.proj_id)
             .all())
        for q_obj in q:
            project = dict()
            project[Projects.proj_id.name] = q_obj.proj_id
            project[Projects.outside_name.name] = q_obj.outside_name
            project[Projects.describe.name] = q_obj.describe
            project[Projects.commit_time.name] = self.time_to_str(q_obj.commit_time)
            project[Projects.update_time.name] = self.time_to_str(q_obj.update_time)
            project[Projects.inside_name.name] = q_obj.insideName.inside_name
            project[Projects.proj_type.name] = q_obj.projectType.project_type
            project[Projects.proj_state.name] = q_obj.projectState.state_name
            project_list.append(project)
        return project_list

    def get_proj_list_by_user_id(self, user_id):
        """
        获取我的项目
        :param project_type:
        :return:
        """
        project_list = []
        q1 = (db.session.query(Projects)
              .outerjoin(UserRole, UserRole.proj_id == Projects.proj_id)
              .filter(UserRole.user_id == user_id)
              .filter(Projects.proj_state != 3)
              .order_by(Projects.proj_id.desc())
              )
        q2 = (db.session.query(Projects)
              .filter(Projects.commit_user == user_id)
              .filter(Projects.proj_state != 3)
              .order_by(Projects.proj_id.desc()))
        q3 = q1.union(q2)
        for proj in q3:
            project_list.append(self.proj_to_dict(proj))
        return project_list

    def proj_to_dict(self, info):
        project = dict()
        project[Projects.proj_id.name] = info.proj_id
        project[Projects.outside_name.name] = info.outside_name
        project[Projects.describe.name] = info.describe
        project[Projects.commit_time.name] = self.time_to_str(info.commit_time)
        project[Projects.update_time.name] = self.time_to_str(info.update_time)
        project[Projects.inside_name.name] = info.insideName.inside_name
        project[Projects.proj_type.name] = info.projectType.project_type
        project[Projects.proj_state.name] = info.projectState.state_name
        return project

    def get_projects_by_id(self, proj_info):
        return

    def get_one_proj_by_id(self, pro_id):
        try:
            proj_info = db.session.query(Projects).filter(Projects.proj_id == pro_id).first()
            observer_info = db.session.query(ProjectObserver).filter(ProjectObserver.proj_id == pro_id).all()
            if proj_info:
                project = proj_info.to_dict()
                project["user_name"] = proj_info.users.user_name
                project["observer_list"] = []
                project["observer_name_list"] = []
                for observer in observer_info:
                    project["observer_list"].append({"value": observer.observer_id, "key": observer.id})
                    project["observer_name_list"].append({"name": observer.users.user_name})
                project["inside_i_name"] = proj_info.insideName.inside_name
                project["proj_i_type"] = proj_info.projectType.project_type
                project["proj_i_state"] = proj_info.projectState.state_name
                project["quotations"] = []
                quotations = proj_info.quotations
                for iq in quotations:
                    quotation = iq.to_dict()
                    from app.ctrl.ctrl_quotations import CtrlQuotations
                    quotation[Quotations.create_user.name] = CtrlQuotations().get_user_name_by_id(iq.create_user)
                    quotation[Quotations.update_user.name] = CtrlQuotations().get_user_name_by_id(iq.create_user)
                    project["quotations"].append(quotation)
                return True, project
            else:
                return False, "沒有此項目信息"
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"

    def change_proj_by_id(self, pro_id, data):
        try:
            proj = (db.session.query(Projects).filter(Projects.proj_id == pro_id).first())
            if proj:
                inside_name = (db.session.query(ProjectInsideName)
                               .filter(ProjectInsideName.inside_name == data.get("inside_name"))
                               .first())
                if inside_name:
                    proj.inside_name = inside_name.inside_id
                proj.insideName.inside_name = data.get("inside_name")
                proj.outside_name = data.get("outside_name")
                proj.proj_type = data.get("proj_type")
                proj.describe = data.get("describe")
                proj.update_time = self.get_current_time()
                db.session.commit()
                return proj.proj_id, ""
            else:
                return False, "沒有此項目"
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"

    def change_proj_by_id_with_observer(self, pro_id, data):
        try:
            outside_name = data.get("outside_name")
            proj_type = data.get("proj_type")
            describe = data.get("describe")
            inside_name = data.get("inside_name")
            observer_list = data.get("observer_list")
            if not outside_name:
                return False, "项目客户名称不能为空"
            if not proj_type:
                return False, "项目系列不能为空"
            if not describe:
                return False, "项目简介不能为空"
            if not inside_name:
                return False, "项目内部名称不能为空"
            proj = (db.session.query(Projects).filter(Projects.proj_id == pro_id).first())
            if proj:
                self.change_proj_value(proj, inside_name, outside_name, proj_type, describe)
                self.change_proj_observer(proj, observer_list)
                db.session.commit()
                return proj.proj_id, ""
            else:
                return False, "沒有此項目"
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"

    def change_proj_value(self, proj, inside_name, outside_name, proj_type, describe):
        """
        :param proj: obj
        :param inside_name: str
        :param outside_name: str
        :param proj_type: str
        :param describe: str
        :return:
        """
        inside_name_obj = (db.session.query(ProjectInsideName)
                           .filter(ProjectInsideName.inside_name == inside_name)
                           .first())
        if inside_name_obj:
            proj.inside_name = inside_name_obj.inside_id
        else:
            proj.insideName.inside_name = inside_name
        proj.proj_type = self.add_proj_type(proj_type)
        proj.outside_name = outside_name
        proj.describe = describe
        proj.update_time = self.get_current_time()

    def change_proj_observer(self, proj, observer_list):
        """
        :param proj: obj
        :param observer_list: list
        :return:
        """
        old_ob_list = (db.session.query(ProjectObserver).filter(ProjectObserver.proj_id == proj.proj_id).all())
        old_list = set([old.observer_id for old in old_ob_list])
        new_list = set([new.get("value") for new in observer_list])
        for old_observer in old_list:
            if old_observer not in new_list:
                (db.session.query(ProjectObserver)
                 .filter(ProjectObserver.proj_id == proj.proj_id)
                 .filter(ProjectObserver.observer_id == old_observer).delete())
                (db.session.query(UserRole)
                 .filter(UserRole.proj_id == proj.proj_id)
                 .filter(UserRole.user_id == old_observer)
                 .filter(UserRole.group_id == 1)
                 .filter(UserRole.role_id == 1).delete())
        for new_observer in new_list:
            if new_observer and (new_observer not in old_list) and (new_observer != proj.commit_user):
                self.add_observer(new_observer, proj.proj_id)

    def update_observer(self, observer, proj_id):
        observer_info = {
            ProjectObserver.proj_id.name: proj_id,
            ProjectObserver.observer_id.name: observer.get("value"),
        }
        role = (db.session.query(UserRole)
                .filter(UserRole.user_id == observer.get("value"))
                .filter(UserRole.role_id == 1)
                .filter(UserRole.group_id == 1).first())
        if not role:
            user_role_info = {
                UserRole.user_id.name: observer.get("value"),
                UserRole.role_id.name: 1,
                UserRole.group_id.name: 1,
            }
            role = UserRole(**user_role_info)
            db.session.add(role)
        pro = ProjectObserver(**observer_info)
        db.session.add(pro)

    def delete_proj_by_id(self, data):
        try:
            proj = (db.session.query(Projects).filter(Projects.proj_id == data.get("proj_id")).first())
            if proj:
                db.session.execute(self.del_manday.format(data.get("proj_id")))
                db.session.execute(self.del_task.format(data.get("proj_id")))
                db.session.execute(self.del_function_one.format(data.get("proj_id")))
                db.session.execute(self.del_function_two.format(data.get("proj_id")))
                db.session.execute(self.del_option_combination.format(data.get("proj_id")))
                db.session.execute(self.del_option_value.format(data.get("proj_id")))
                db.session.execute(self.del_options.format(data.get("proj_id")))
                db.session.execute(self.del_preconditions.format(data.get("proj_id")))
                db.session.execute(self.del_quotations.format(data.get("proj_id")))
                db.session.execute(self.del_user_role.format(data.get("proj_id")))
                db.session.execute(self.del_project_observer.format(data.get("proj_id")))
                db.session.execute(self.del_projects.format(data.get("proj_id")))
                db.session.commit()
                return True, ""
            else:
                return False, "沒有此項目"
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"

    def project_basic_messige(self, proj_id):
        """取项目基本信息"""
        project = dict()
        q = db.session.query(Projects).filter(Projects.proj_id == proj_id).first()
        if q:
            project[Projects.proj_id.name] = proj_id
            project[Projects.inside_name.name] = q.insideName.inside_name
            project[Projects.outside_name.name] = q.outside_name
            project[Projects.commit_user.name] = q.users.to_dict()
        return project

    def get_manager_list(self):
        q = db.session.query(Projects).all()
        manage_list = []
        try:
            for proj in q:
                manage = dict()
                manage["manage_id"] = proj.proj_id
                manage["manage_name"] = "-".join([proj.insideName.inside_name, '体制表'])
                manage_list.append(manage)
            return True, manage_list
        except Exception as e:
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"

    def import_manager(self, request_data):
        result = dict()
        try:
            file_upload = request_data.files['file']
            uti = Utillity()
            only_id = uti.get_nextval("file_seq_file_id_seq")
            file_path = "manager_import"
            file_path = os.path.join(file_path, str(only_id))
            file_path = os.path.abspath(os.path.join(os.getcwd(), file_path))
            file_name = file_upload.filename
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            file_url = os.path.join(file_path, file_name)
            file_upload.save(file_url)
            result["file"] = {
                "file_name": file_name,
                "file_url": file_url,
            }
            return result, ''
        except Exception as e:
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"

    def get_project_manager(self, proj_id, user_id):
        """
        取项目的体制信息
        :param proj_id:
        :return:
        """
        from app.ctrl.ctrl_user_group import CtrlUserGroup
        ctrl_group = CtrlUserGroup()
        try:
            project_data = self.project_basic_messige(proj_id)
            proj_id = project_data.get("proj_id")
            proj_name = project_data.get("inside_name")
            owner_user = project_data.get("commit_user")
            proj_manager = {"proj_id": proj_id, "proj_name": proj_name,
                            "owner_user": owner_user, "permissions": []}
            leader = 0
            if owner_user.get("user_id") == user_id:
                leader = 1
            if leader:
                proj_manager["permissions"] = ["PERM-PROJECTGROUP-LIST"]
            # 取pl组
            pl_group = ctrl_group.get_pl_group(owner_user.get("user_id"), proj_id)
            if not pl_group:
                pl_group = ctrl_group.get_pl_group(owner_user.get("user_id"))
                proj_manager["group_id"] = pl_group.get("group_id")
                proj_manager["group_name"] = pl_group.get("group_name")
                proj_manager["sub"] = []
                return proj_manager, ""
            proj_manager["group_id"] = pl_group.get("group_id")
            proj_manager["group_name"] = pl_group.get("group_name")
            # proj_manager["members"] = ctrl_group.group_members(pl_group.get("group_id"), owner_user.get("user_id"))
            # 取SGL，GL
            parent_group_id = pl_group.get("group_id")
            proj_manager["sub"] = []
            self.get_sub_group(parent_group_id, ctrl_group, proj_id, proj_manager["sub"], leader, user_id)
            return True, proj_manager
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"

    def get_sub_group(self, parent_group_id, ctrl_group, proj_id, group_list, leader, user_id):
        from app.ctrl.ctrl_user import CtrlUser
        ctrl_user = CtrlUser()
        sub_q = (db.session.query(Group.group_id, Group.group_name,
                                  Group.owner_user, UserRole.user_id)
                 .outerjoin(UserRole, Group.group_id == UserRole.group_id)
                 .filter(Group.parent_group_id == parent_group_id)
                 .filter(UserRole.proj_id == proj_id)
                 .order_by(Group.group_name).all())
        if sub_q:
            for sub in sub_q:
                sub_group = dict()
                sub_group['group_id'] = sub.group_id
                sub_group['group_name'] = sub.group_name
                sub_group['owner_user'] = ctrl_user.get_one_user(sub.user_id)
                if leader:
                    sub_leader = True
                    sub_group['members'] = ctrl_group.group_members(sub.group_id, sub.owner_user)
                    sub_group["permissions"] = ["PERM-PROJECTGROUP-LIST"]
                else:
                    if user_id == sub.user_id:
                        sub_leader = True
                        sub_group['members'] = ctrl_group.group_members(sub.group_id, sub.owner_user)
                        sub_group["permissions"] = ["PERM-PROJECTGROUP-LIST"]
                    else:
                        sub_leader = False
                        sub_group['members'] = []
                        sub_group["permissions"] = []
                sub_group['sub'] = []
                self.get_sub_group(sub.group_id, ctrl_group, proj_id, sub_group['sub'], sub_leader, user_id)
                group_list.append(sub_group)
        else:
            return

    def import_project_manager(self, file_url, proj_id):
        curr_app = current_app._get_current_object()
        from app.ctrl.ctrl_user_group import CtrlUserGroup
        ctrl_group = CtrlUserGroup()
        from app.ctrl.ctrl_user import CtrlUser
        ctrl_user = CtrlUser()
        project_data = self.project_basic_messige(proj_id)
        proj_owner_user = project_data.get("commit_user")
        pl_group = ctrl_group.get_pl_group(proj_owner_user.get("user_id"))
        pl_group_id = pl_group.get("group_id")
        ctrl_import = ImportManager()
        success, manager_df = ctrl_import.import_excel(file_url)
        if not success:
            return False, manager_df
        manager_group = manager_df.to_dict(orient='records')
        manager_list = [{"role_id": curr_app.config.get("SALES_ROLE_ID"), "user_id": proj_owner_user.get("user_id"),
                         "proj_id": proj_id, "group_id": pl_group_id}]
        group_tree = self.get_group_tree(manager_group)
        for group in group_tree:
            group_name = group.get("group_name")
            owner_user = group.get("owner_user")
            sub_group = group.get("sub")
            sgl_obj, error = ctrl_user.add_user(owner_user)
            if error:
                return False, error
            sgl_user_id = sgl_obj.user_id
            sgl_group = {"group_name": group_name, "describe": "",
                         "parent_group_id": pl_group_id, "owner_user": sgl_user_id}
            res, msg = ctrl_group.add_group(sgl_group)
            if res:
                sgl_group_id = msg
            else:
                db.session.rollback()
                return False, msg
            manager_list.append({"role_id": curr_app.config.get("SGL_ROLE_ID"), "user_id": sgl_user_id,
                                 "proj_id": proj_id, "group_id": sgl_group_id})
            for sub in sub_group:
                gl_obj, error = ctrl_user.add_user(sub.get("owner_user"))
                if error:
                    return False, error
                gl_user_id = gl_obj.user_id
                gl_group = {"group_name": sub.get("group_name"), "describe": "",
                            "parent_group_id": sgl_group_id, "owner_user": gl_user_id}
                res, msg = ctrl_group.add_group(gl_group)
                if res:
                    gl_group_id = msg
                else:
                    db.session.rollback()
                    return False, msg
                manager_list.append({"role_id": curr_app.config.get("GL_ROLE_ID"), "user_id": gl_user_id,
                                     "proj_id": proj_id, "group_id": gl_group_id})
        ctrl_group.update_project_manager(proj_id, manager_list)
        return True, ""

    def get_group_tree(self, manager_group):
        group_tree = []
        group_index = dict()
        for group in manager_group:
            group_name = group.get("Group")
            owner_user = group.get("Leader")
            sub_group_name = group.get("SubGroup")
            sub_owner_user = group.get("SubLeader")
            if group_name:
                if group_index.get(group_name):
                    group_dict = group_tree[group_index.get(group_name)]
                    group_dict["sub"].append({"group_name": sub_group_name,
                                              "owner_user": sub_owner_user})
                else:
                    group_dict = dict()
                    group_dict["group_name"] = group_name
                    group_dict["owner_user"] = owner_user
                    group_dict["sub"] = []
                    if sub_group_name:
                        group_dict["sub"].append({"group_name": sub_group_name,
                                                  "owner_user": sub_owner_user})
                    group_tree.append(group_dict)
                    group_index[group_name] = len(group_tree) - 1
        return group_tree














