from app.db import db
import pandas as pd
from flask import current_app
from app.db.users import Group, Users, Roles
from app.db.users import UserRole
from app.data_server.ds_pieces import get_group_df
from app.ctrl.ctrl_base import CtrlBase
from app.data_server.ds_pieces import refresh_group_df
from sqlalchemy import or_, and_,  func


class CtrlUserGroup(CtrlBase):
    def __init__(self):
        CtrlBase.__init__(self)

    # 查询所有的组
    def get_all_groups(self):
        group_df = get_group_df()
        group_df = group_df[~group_df['group_id'].isin([1])]  # 反选不是PL的组
        return group_df.to_dict(orient="records")

    def get_project_groups_tree(self, proj_id):
        curr_app = current_app._get_current_object()
        q = (db.session.query(Group)
             .outerjoin(UserRole, Group.group_id == UserRole.group_id)
             .filter(UserRole.proj_id == proj_id)
             .filter(UserRole.role_id == curr_app.config.get("SGL_ROLE_ID"))
             .order_by(Group.group_name))
        group_q = (db.session.query(Group)
                   .outerjoin(UserRole, Group.group_id == UserRole.group_id)
                   .filter(UserRole.proj_id == proj_id)
                   .order_by(Group.group_name))
        group_df = pd.read_sql(group_q.statement, db.session.bind)
        group_list = []
        for group in q:
            group_dict = dict()
            group_dict[Group.group_id.name] = group.group_id
            group_dict[Group.group_name.name] = group.group_name
            sub_group_df = group_df[group_df[Group.parent_group_id.name] == group.group_id]
            group_dict["sub"] = sub_group_df.to_dict(orient="records")
            group_list.append(group_dict)
        return group_list

    def get_project_groups(self, proj_id):
        q = (db.session.query(Group)
             .outerjoin(UserRole, Group.group_id == UserRole.group_id)
             .filter(UserRole.proj_id == proj_id)
             .order_by(Group.group_name))
        group_list = []
        for group in q:
            group_dict = dict()
            group_dict[Group.group_id.name] = group.group_id
            group_dict[Group.group_name.name] = group.group_name
            group_list.append(group_dict)
        return group_list

    def get_group_by_name(self, group_name):
        """查询排除掉系统默认的PL组"""
        q = (db.session.query(Group)
             .filter(Group.group_name == group_name)
             .filter(Group.group_id != 1)
             .first())
        return q

    def group_name_dict(self):
        """
        获取组{name:id}的字典信息
        :return:
        """
        group_df = get_group_df()
        group_list = group_df.to_dict(orient="records")
        group_dict = dict()
        for group in group_list:
            group_dict[group.get("group_name")] = group.get("group_id")
        return group_dict

    # 查当前组下的所有user及其role
    # def get_users_by_group(self, group_id):
    #     group_obj = db.session.query(Group.group_name).filter(Group.group_id == group_id).first()
    #     group_members = group_obj.group_members
    #     leader = ""
    #     members = []
    #     for member in group_members:
    #         if member
    #     user_id = db.session.query(user_role.user_id).filter(user_role.group_id == group_id).all()
    #     usrname_rolename_list = []
    #     for q in user_id:
    #         current_role_name = db.session.query(Roles.role_name).filter(Roles.user_id == q).first()
    #         current_user_name = db.session.query(Users.user_name).filter(Users.user_id == q).first()
    #         usrname_rolename_list.append([current_role_name, current_user_name])
    #     return {group_name: usrname_rolename_list}

    def get_my_group(self, user_id, proj_id=None):
        """

        :param user_id:
        :param proj_id:
        :return:
        """
        q = (db.session.query(Group)
             .outerjoin(UserRole, Group.group_id == UserRole.group_id)
             .filter(UserRole.user_id == user_id))
        if proj_id:
            q = q.filter(UserRole.proj_id == proj_id)
        # q = q.first()
        group_list = []
        for group in q:
            group_list.append(group.to_dict())
        return group_list
        # else:
        #     group_list = []
        #     for q_obj in q:
        #         group_list.append(q_obj.to_dict())
        #     return group_list

    def get_pl_group(self, user_id, proj_id=None):
        q = (db.session.query(Group)
             .outerjoin(UserRole, Group.group_id == UserRole.group_id)
             .filter(Group.group_name == "PL")
             .filter(UserRole.user_id == user_id))
        if proj_id:
            q = q.filter(UserRole.proj_id == proj_id)
        q = q.first()
        if q:
            return q.to_dict()
        else:
            return None

    def group_name(self, group_id):
        q = db.session.query(Group).filter(Group.group_id == group_id).first()
        return q.group_name

    def get_group_detail(self, group_id):
        group_data = {"group_id": group_id, "group_name": "", "pl": "",
                      "group_member": []}
        q_list = (db.session.query(Users.user_id, Users.user_name, Users.email, Group.group_name, Roles.role_name)
                  .outerjoin(UserRole, Users.user_id == UserRole.user_id)
                  .outerjoin(Group, UserRole.group_id == Group.group_id)
                  .outerjoin(Roles, UserRole.role_id == Roles.role_id)
                  .filter(UserRole.group_id == group_id))
        for q in q_list:
            user_id = q[0]
            user_name = q[1]
            email = q[2]
            group_name = q[3]
            role_name = q[4]
            if role_name == "PL":
                group_data["pl"] = {"user_id": user_id, "user_name": user_name,
                                    "email": email, "group_name": group_name, "role_name": role_name}
            else:
                group_data["group_member"].append({"user_id": user_id, "user_name": user_name,
                                                   "email": email, "group_name": group_name, "role_name": role_name})
        return group_data

    def group_members(self, group_id, owner_user=0):
        """
        取一个组的成员
        :param group_id:
        :param owner_user:
        :return:
        """
        group_members = []
        group_q = (db.session.query(Users)
                   .outerjoin(UserRole, Users.user_id == UserRole.user_id)
                   .filter(UserRole.group_id == group_id))
        if owner_user:
            group_q = group_q.filter(UserRole.user_id != owner_user)
        for member in group_q:
            group_members.append(member.to_dict())
        return group_members

    def get_user_role(self, proj_id, group_id):
        """获取一个人的角色"""
        q = (db.session.query(Roles)
             .outerjoin(UserRole, Roles.role_id == UserRole.role_id)
             .filter(UserRole.proj_id == proj_id)
             .filter(UserRole.group_id == group_id).first())
        if q:
            return q.role_name
        else:
            return None

    def add_group(self, group_data, commit_list=[]):
        group_id = group_data.get("group_id")
        group_name = group_data.get("group_name")
        parent_group_id = group_data.get("parent_group_id")
        old_group = None
        old_group_q = self.get_group_by_name(group_name)
        if group_id:
            if old_group_q:
                old_group = old_group_q.to_dict()
                if group_id != old_group.get("group_id"):
                    return False, "同个项目中组名不能重复！"
            else:
                old_group_list = self.get_old_data(Group, Group.group_id, group_id)
                if old_group_list:
                    old_group = old_group_list[0]
        if old_group:
            group_data["group_id"] = old_group.get("group_id")
            old_parent_group_id = old_group.get("parent_group_id")
            if parent_group_id != old_parent_group_id:
                return False, "该组已存在父级组！"
        log_dict = self.common_add(Group, group_data, old_group,
                                   [Group.group_name.name, Group.owner_user.name], Group.group_id)
        if log_dict:
            commit_list.append(log_dict)
            group_id = log_dict.get("key_id")
        else:
            group_id = old_group.get("group_id")
        return True, group_id

    def update_project_manager(self, proj_id, data_list):
        self.delete_project_manager(proj_id)
        old_data_list = []
        self.add_list(UserRole, data_list, old_data_list, UserRole.id, [])

    def delete_project_manager(self, proj_id):
        old_data_list = self.get_old_data(UserRole, UserRole.proj_id, proj_id)
        new_data_list = []
        self.add_list(UserRole, new_data_list, old_data_list, UserRole.id, [])

    def update_manager_group(self, data_json):
        curr_app = current_app._get_current_object()
        commit_user = data_json.get("commit_user")
        update_time = self.get_current_time()
        proj_id = data_json.get("proj_id")
        group_id = data_json.get("group_id")
        group_name = data_json.get("group_name")
        parent_group_id = data_json.get("parent_group_id")
        owner_user = data_json.get("owner_user")
        old_owner_user = 0
        try:
            if not parent_group_id:
                return False, "没有指定父级组！"
            parent_group = db.session.query(Group).filter(Group.group_id == parent_group_id).first()
            commit_list = []
            if parent_group.group_name == "PL":
                role_id = curr_app.config.get("SGL_ROLE_ID")
                msg = self.check_manager_group(parent_group.group_id, proj_id)
                if not msg:
                    pl_group_manger = {"id": 0, "proj_id": proj_id, "group_id": parent_group.group_id,
                                       "user_id": parent_group.owner_user,
                                       "role_id": role_id}
                    log_dict = self.common_add(UserRole, pl_group_manger, None,
                                               [UserRole.group_id.name, UserRole.user_id.name], UserRole.id)
                    commit_list.append(log_dict)
            else:
                # parent_user = parent_group.owner_user
                parent_role = self.get_user_role(proj_id, parent_group_id)
                role_id = self.judge_sub_role(parent_role, curr_app)
            if not role_id:
                return False, "该级别无法再添加组！"
            if not group_id:
                group_obj = self.get_group_by_name(group_name)
                if group_obj:
                    group_id = group_obj.group_id
                    # 检查该组是否已存在该项目中
                    msg = self.check_manager_group(group_id, proj_id)
                    if msg:
                        return False, msg
                    old_owner_user = group_obj.owner_user
            else:
                group_obj = db.session.query(Group).filter(Group.group_id == group_id).first()
                old_owner_user = group_obj.owner_user
            new_group = {"group_id": group_id, "group_name": group_name,
                         "parent_group_id": parent_group_id,
                         "owner_user": owner_user}

            # 更新组信息
            res, msg = self.add_group(new_group, commit_list)
            if not res:
                db.session.rollback()
                return False, msg
            group_id = msg
            new_manager = {"id": 0, "proj_id": proj_id, "group_id": group_id,
                           "user_id": owner_user, "role_id": role_id}
            old_manager = None
            if old_owner_user:
                old_manager_list = self.get_old_data(UserRole, [UserRole.proj_id, UserRole.group_id, UserRole.user_id],
                                                     {"proj_id": proj_id, "group_id": group_id,
                                                      "user_id": old_owner_user, "role_id": role_id})
                if old_manager_list:
                    old_manager = old_manager_list[0]
                    new_manager["id"] = old_manager.get("id")
            # 更新组负责人体制信息
            log_dict = self.common_add(UserRole, new_manager, old_manager,
                                       [UserRole.group_id.name, UserRole.user_id.name], UserRole.id)
            if log_dict:
                commit_list.append(log_dict)
            self.commit_log(commit_list, commit_user, update_time)
            db.session.commit()
            refresh_group_df()
            return True, group_id
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"

    def delete_manager_group(self, proj_id, group_id, commit_user):
        try:
            res, msg = self.check_group_assign(proj_id, group_id)
            if not res:
                return res, msg
            old_data_list = self.get_old_data(UserRole, [UserRole.proj_id, UserRole.group_id],
                                              {"proj_id": proj_id, "group_id": group_id})
            commit_list = self.add_list(UserRole, [], old_data_list, UserRole.id, [])
            update_time = self.get_current_time()
            self.commit_log(commit_list, commit_user, update_time)
            db.session.commit()
            refresh_group_df()
            return True, ""
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"

    def check_group_assign(self, proj_id, group_id):
        """检查组是否被分配"""
        from app.db.quotations import Quotations, Functions, FuncGroup, Task, FuncManDay
        # 检查是否有Feature分配
        check_q1 = (db.session.query(Group)
                    .outerjoin(FuncGroup, Group.group_id == FuncGroup.group_id)
                    .outerjoin(Functions, FuncGroup.func_id == Functions.func_id)
                    .outerjoin(Quotations, Functions.quotation_id == Quotations.quotation_id)
                    .filter(Quotations.proj_id == proj_id)
                    .filter(FuncGroup.group_id == group_id).first())
        # 检查是否有TASK分配
        check_q2 = (db.session.query(Group)
                    .outerjoin(Task, Group.group_id == Task.group_id)
                    .outerjoin(Functions, Task.func_id == Functions.func_id)
                    .outerjoin(Quotations, Functions.quotation_id == Quotations.quotation_id)
                    .filter(Quotations.proj_id == proj_id)
                    .filter(Task.group_id == group_id).first())
        mayday_q = (db.session.query(FuncManDay.task_id, FuncManDay.group_id,
                                     FuncManDay.option_id,
                                     func.max(FuncManDay.id))
                    .outerjoin(Task, FuncManDay.task_id == Task.task_id)
                    .outerjoin(Functions, Task.func_id == Functions.func_id)
                    .outerjoin(Quotations, Functions.quotation_id == Quotations.quotation_id)
                    .filter(Quotations.proj_id == proj_id)
                    .filter(FuncManDay.group_id == group_id)
                    .group_by(FuncManDay.task_id, FuncManDay.group_id,
                              FuncManDay.option_id).all()
                    )  # 取关于我的task的所填的最新工数
        manday_ids = [q[3] for q in mayday_q]  # 取最新版本工数的id
        # 检查是否有填写工数
        check_q3 = (db.session.query(Group)
                    .outerjoin(FuncManDay, Group.group_id == FuncManDay.group_id)
                    .filter(FuncManDay.id.in_(manday_ids))
                    .filter(or_(FuncManDay.days.isnot(None),
                                and_(FuncManDay.comment.isnot(None), FuncManDay.comment != ""),
                                FuncManDay.pre_id.isnot(None),
                                FuncManDay.status_id.isnot(None)
                                )).first())
        if check_q1 or check_q2 or check_q3:
            return False, "该组已经被分配或存在工数, 请先取消分配或清空工数信息！"
        else:
            return True, ""

    def update_manager_member(self, data_json):
        commit_user = data_json.get("commit_user")
        update_time = self.get_current_time()
        proj_id = data_json.get("proj_id")
        group_id = data_json.get("group_id")
        user_id = data_json.get("user_id")
        try:
            msg = self.check_manager_member(group_id, user_id, proj_id)
            if not msg:
                return False, msg
            new_manager = {"proj_id": proj_id, "group_id": group_id,
                           "user_id": user_id, "id": 0}
            commit_list = self.add_list(UserRole, [new_manager], [], UserRole.id, [])
            self.commit_log(commit_list, commit_user, update_time)
            db.session.commit()
            return True, ""
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"

    def delete_manager_member(self, proj_id, group_id, user_id, commit_user):
        try:
            old_data_list = self.get_old_data(UserRole, [UserRole.proj_id, UserRole.group_id, UserRole.user_id],
                                              {"proj_id": proj_id, "group_id": group_id, "user_id": user_id})
            commit_list = self.add_list(UserRole, [], old_data_list, UserRole.id, [])
            update_time = self.get_current_time()
            self.commit_log(commit_list, commit_user, update_time)
            db.session.commit()
            return True, ""
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"

    def check_manager_group(self, group_id, proj_id):
        q = (db.session.query(UserRole)
             .filter(UserRole.proj_id == proj_id)
             .filter(UserRole.group_id == group_id)
             .all())
        if q:
            return "该组已存在项目中！"
        return None

    def check_manager_member(self, group_id, user_id, proj_id):
        q = (db.session.query(UserRole)
             .filter(UserRole.proj_id == proj_id)
             .filter(UserRole.group_id == group_id)
             .filter(UserRole.user_id == user_id)
             .all())
        if q:
            return "该成员已在组内！"
        return None

    def judge_sub_role(self, parent_role, curr_app):
        if parent_role == "SALES":
            return curr_app.config.get("SGL_ROLE_ID")
        elif parent_role == "SGL":
            return curr_app.config.get("GL_ROLE_ID")
        else:
            return False

    def get_groups_by_proj(self, role_id, proj_id):
        """
        根据角色和项目确定组
        :param role_id: 角色ID
        :param proj_id: 项目ID
        :return:
        """
        group_list = []
        q = (db.session.query(UserRole)
             .filter(UserRole.proj_id == proj_id)
             .filter(UserRole.role_id == role_id)
             .all())
        if q:
            for group in q:
                g = db.session.query(Group).filter(Group.group_id == group.group_id).first()
                group_info = dict()
                group_info["group_name"] = g.group_name
                group_info["group_id"] = g.group_id
                group_list.append(group_info)
        return group_list

    def get_sub_groups(self, group_ids):
        """"""
        group_list = []
        q = (db.session.query(Group)
             .filter(Group.parent_group_id.in_(group_ids))
             .all())
        if q:
            for group in q:
                group_info = dict()
                group_info["group_name"] = group.group_name
                group_info["group_id"] = group.group_id
                group_info[Group.owner_user.name] = group.owner_user
                group_list.append(group_info)
        return group_list

    def get_project_sgl_group(self, proj_id):
        curr_app = current_app._get_current_object()
        sgl_role_id = curr_app.config.get("SGL_ROLE_ID")
        sgl_group_list = []
        q_group = (db.session.query(Group)
                   .outerjoin(UserRole, Group.group_id == UserRole.group_id)
                   .filter(UserRole.proj_id == proj_id)
                   .filter(UserRole.role_id == sgl_role_id)
                   .order_by(Group.group_name)
                   )
        for group in q_group:
            sgl_group_list.append(group.to_dict())
        return sgl_group_list











