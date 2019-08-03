import os, datetime
import pandas as pd
import numpy
import copy
import xlsxwriter
from app.ctrl.ctrl_task import CtrlTask
from app.db.quotations import *
from app.data_server.ds_quotation import get_ds_quotation
from app.db.quotations import OptionCombination
from app.db.users import Group, UserRole
from app.ctrl.ctrl_user_group import CtrlUserGroup
from app.db.users import Users, Roles
from app.data_server.ds_pieces import get_group_df, get_gl_sgl_df
from app.data_server.ds_quotation import refresh_ds_quotation
from app.data_server.ds_quotation import refresh_lastest_man_day_id
from app.ctrl.ctrl_user import CtrlUser
from flask import current_app
from flask import send_from_directory
# import os
# from flask import Flask


class CtrlCost(CtrlTask):
    def __init__(self):
        CtrlTask.__init__(self)
        self.key_col = FuncManDay.id
        self.db_object = FuncManDay
        self.col_list = [FuncManDay.pre_id.name, FuncManDay.status_id.name, FuncManDay.group_id.name,
                         FuncManDay.comment.name, FuncManDay.days.name]

    def func_task_merge_group(self, func_task_df, proj_id):
        group_df = get_group_df()
        gl_sgl_df = get_gl_sgl_df(proj_id)
        gl_sgl_df.drop(['group_name', 'parent_group_id'], axis=1, inplace=True)
        func_task_merge_group = pd.merge(func_task_df, group_df,
                                         left_on="group_id", right_on="group_id",
                                         how="left")
        func_task_merge_group = pd.merge(func_task_merge_group, gl_sgl_df,
                                         left_on="group_id", right_on="group_id",
                                         how="left")
        return func_task_merge_group

    def get_quotations_cost(self, quotation_id, user_id, myself):
        """根据报价取task和工数信息"""
        q_obj = self.get_quotation_by_id(quotation_id)
        result = dict()
        if q_obj:
            proj_id = q_obj.proj_id
            quotation_name = q_obj.quotation_name
            quotation_ver = q_obj.quotation_ver
            proj_obj = q_obj.projects
            proj_name = proj_obj.insideName.inside_name
            # my_groups = CtrlUserGroup().get_my_group(user_id, proj_id)
            # my_group_ids = [group.get("group_id") for group in my_groups]
            cost_list = ["days", "precondition", "comment", "status"]
            data_list = []
            select_data = dict()
            select_data["precondition"] = self.get_all_precondition(proj_id)
            option_list, option_ids = self.get_option_list(quotation_id)
            group_list_df = get_gl_sgl_df(proj_id)
            parent_group_id_list = group_list_df["parent_group_id"].tolist()
            role_list = CtrlUser().get_user_roles(user_id, proj_id)
            out_project_roles = CtrlUser().out_project_user_roles(user_id)  # 项目之外的用户角色
            my_role = None
            if 'SuperPL' in out_project_roles:
                my_role = "SuperPL"
            elif 'SALES' in role_list:
                my_role = "SALES"
            elif "SGL" in role_list:
                my_role = "SGL"
            elif "GL" in role_list:
                my_role = "GL"
            if my_role in ("SALES", "SuperPL"):
                all_group = CtrlUserGroup().get_all_groups()
                group_id_list = [group.get("group_id") for group in all_group]
                # group_id_list.remove(1)  # 去掉pl组
            else:
                group_id_list = self.get_my_and_sub_group_owner_users(user_id, proj_id)
            group_list, group_ids, parent_sub_group_ids = self.get_group_list_by_df(group_id_list, q_obj.proj_id, parent_group_id_list)
            select_data['status'] = self.get_status_by_role(my_role)
            option_name_list = [option.get("option_name") for option in option_list]
            group_name_list = [group.get("group_name") for group in group_list]
            group_name_list = sorted(list(set(group_name_list)), key=lambda v: v.lower())  # 按组名称排序
            obj_quotation = get_ds_quotation(quotation_id)
            func_task_df, manday_dict = obj_quotation.filter_and_split_manday_df(set(group_ids),
                                                                                 set(parent_sub_group_ids),
                                                                                 option_ids,
                                                                                 my=myself
                                                                                 # my_group_id=my_group_ids,
                                                                                 # my_role=my_role
                                                                                 )
            # func_task_merge_group = func_task_df
            func_task_merge_group = self.func_task_merge_group(func_task_df, proj_id)
            func_task_merge_group = func_task_merge_group.fillna('')
            option_group = []
            for option in option_list:
                option_id = option.get("option_id")
                option_name = option.get("option_name")
                for group in group_list:
                    group_id = group.get("group_id")
                    group_name = group.get("group_name")
                    option_group.append(((option_id, group_id), (option_name, group_name)))
            for i in range(len(func_task_merge_group)):
                func_task_dict = func_task_merge_group.iloc[i].to_dict()
                self.to_int(func_task_dict)
                group_name = func_task_dict.get("group_name")
                sgl_group_name = func_task_dict.get("parent_group_name")
                if sgl_group_name:
                    func_task_dict["group_name_list"] = [sgl_group_name, group_name]
                else:
                    func_task_dict["group_name_list"] = [group_name]
                # func_task_dict = self.find_children_group([func_task_dict])[0]
                cost_dict = self.get_cost_data(option_group, manday_dict, i)
                func_task_dict.update(cost_dict)
                data_list.append(func_task_dict)
            result["cost_list"] = cost_list
            result["data_list"] = data_list
            result["option_list"] = option_name_list
            result["group_list"] = group_name_list
            result["select_data"] = select_data
            result["proj_id"] = proj_id
            result["proj_name"] = proj_name
            result["quotation_name"] = quotation_name
            result["quotation_ver"] = quotation_ver
            # TODO 有过滤条件时把实际返回的Feature/Task DataFrame作为参数传进来
            if myself:
                result["func_task_list"] = (obj_quotation.get_func_columns(func_task_df) +
                                            obj_quotation.get_task_columns(func_task_df) +
                                            ["分配大组", "分配小组"])
            else:
                result["func_task_list"] = (obj_quotation.get_func_columns() +
                                            obj_quotation.get_task_columns() +
                                            ["分配大组", "分配小组"])
            return True, result
        else:
            return False, "该报价不存在！"

    def get_status_by_role(self, role_name):
        status_list = []
        curr_app = current_app._get_current_object()
        if role_name in ("SALES", "SuperPL"):
            status_list = curr_app.config.get("SALES_STATUS_LIST")
        elif role_name == "SGL":
            status_list = curr_app.config.get("SGL_STATUS_LIST")
        elif role_name == "GL":
            status_list = curr_app.config.get("GL_STATUS_LIST")
        return status_list

    def to_int(self, data_dict):
        for key in data_dict:
            if type(data_dict[key]) in (numpy.int32, numpy.int64):
                data_dict[key] = int(data_dict.get(key))
            elif type(data_dict[key]) in (numpy.float, numpy.float32, numpy.float64):
                data_dict[key] = float(data_dict.get(key))
            elif type(data_dict[key]) == numpy.bool_:
                data_dict[key] = bool(data_dict.get(key))

    def get_option_list(self, quotation_id):
        option_list = []
        option_ids = []
        q = (db.session.query(OptionCombination)
             .filter(OptionCombination.quotation_id == quotation_id)
             .order_by(OptionCombination.id))
        for q_obj in q:
            option_ids.append(q_obj.id)
            option_list.append({"option_id": q_obj.id, "option_name": q_obj.value})
        return option_list, option_ids

    def get_cost_data(self, option_group, manday_dict, i):
        cost_dict = dict()
        for (option_id, group_id), (option_name, group_name) in option_group:
            manday_df = manday_dict.get((option_id, group_id))
            if manday_df is not None:
                s = manday_df.iloc[i]
                s_dict = s.to_dict()
                self.to_int(s_dict)
                cost_dict.setdefault(option_name, dict())[group_name] = self.cost_to_dict(s_dict)
            else:
                cost_dict.setdefault(option_name, dict())[group_name] = {"id": 0, "days": None,
                                                                         "base_id": 0,
                                                                         "precondition": None, "comment": None,
                                                                         "status": None, "issue_status": None}
        # for option in option_list:
        #     option_id = option.get("option_id")
        #     option_name = option.get("option_name")
        #     option_dict = dict()
        #     for group in group_list:
        #         group_id = group.get("group_id")
        #         group_name = group.get("group_name")
        #
        #     cost_dict[option_name] = option_dict
        return cost_dict

    def cost_to_dict(self, cost_dict):
        self.to_int(cost_dict)
        new_cost_dict = dict()
        new_cost_dict["id"] = cost_dict.get("id")
        new_cost_dict["base_id"] = cost_dict.get("base_id")
        new_cost_dict["days"] = cost_dict.get("days")
        new_cost_dict["precondition"] = cost_dict.get("precondition")
        new_cost_dict["comment"] = cost_dict.get("comment")
        new_cost_dict["status"] = cost_dict.get("status")
        new_cost_dict["issue_status"] = cost_dict.get("issue_status")
        return new_cost_dict

    def update_cost(self, data_json):
        """更新工数信息"""
        update_time = self.get_current_time()
        # proj_id = data_json.get("proj_id")
        quotation_id = data_json.get("quotation_id")
        q_obj = self.get_quotation_by_id(quotation_id)
        if not q_obj:
            return False, "该报价不存在！"
        proj_id = q_obj.proj_id
        commit_user = int(data_json.get("commit_user"))
        select_data = data_json.get("select_data")
        precondition_list = select_data.get("precondition")
        data_list = data_json.get("data_list")
        option_list = data_json.get("option_list")
        delete_task_list = data_json.get("delete_list")
        # 更新前提数据库
        try:
            self.add_new_precondition(precondition_list, proj_id, quotation_id)
            res, msg = self.delete_task(delete_task_list)
            if not res:
                return False, msg
            commit_list = []
            last_task = dict()  # 上一个task信息，为了补全上级task信息
            last_func_id = 0  # 上一个func_id, 与上一条task的func_id相同时才继承上级task信息
            for data in data_list:
                func_id = data.get("func_id")
                if func_id != last_func_id:
                    last_task = dict()
                group_list = data.get("group_name_list")
                option_dict, task_dict = self.decomposition_data(data, option_list, commit_user, proj_id, update_time)
                self.completion_task(task_dict, last_task)
                last_func_id = func_id
                last_task = copy.deepcopy(task_dict)  # 复制该条task信息
                action = data.get("action")
                if action == "change":  # 说明该条是新增的或者有变更
                    task_id = task_dict.get("task_id")
                    if group_list:
                        res, msg = self.check_group_in_manager(group_list[-1], proj_id)
                        if not res:
                            db.session.rollback()
                            return False, msg
                        else:
                            task_dict["group_id"] = msg
                    else:
                        task_dict["group_id"] = None
                    res, msg = self.update_one_task(task_dict, action)
                    if res:
                        log_dict = msg
                        if log_dict:
                            task_id = log_dict.get("key_id")
                            commit_list.append(log_dict)
                    else:
                        db.session.rollback()
                        return False, msg
                    # 更新工数
                    commit_list += self._updaet_cost(task_id, option_dict, quotation_id,
                                                     proj_id, update_time, commit_user)
            self.commit_log(commit_list, commit_user, update_time)
            refresh_lastest_man_day_id()
            db.session.commit()
            refresh_ds_quotation(quotation_id)
            return True, ""
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % e)
            return False, "服务异常！%s" % str(e)

    def decomposition_data(self, data_dict, option_list, commit_user, proj_id, update_time):
        """
        拆分工数和task信息
        :param data_json:
        :param option_list:
        :return:
        """
        option_dict = dict()
        task_dict = dict()
        for key in data_dict:
            if key in self.task_col_list:
                val = data_dict.get(key)
                if val and isinstance(val, str):
                    val = val.strip()  # 去掉尾部空格
                if val == '':
                    task_dict[key] = None
                else:
                    task_dict[key] = val
            if key in option_list:
                option_dict[key] = data_dict.get(key)
        if not task_dict.get("task_id"):
            task_dict[Task.create_user.name] = commit_user
            # if not task_dict.get("group_id"):
            #     group_dict = CtrlUserGroup().get_my_group(commit_user, proj_id)
            #     if group_dict:
            #         task_dict["group_id"] = [group_dict.get("group_id")]
        if task_dict.get(Task.group_id.name) == "":
            task_dict[Task.group_id.name] = None
        task_dict[Task.update_user.name] = commit_user
        task_dict[Task.update_time.name] = update_time
        return option_dict, task_dict

    def _updaet_cost(self, task_id, option_dict, quotation_id,
                     proj_id, update_time, commit_user):
        commit_list = []
        group_name_dict = CtrlUserGroup().group_name_dict()
        for option in list(option_dict.keys()):
            option_id = self.get_option_id(option, quotation_id)
            group_dict = option_dict.get(option)
            for group in list(group_dict.keys()):
                group_id = group_name_dict.get(group)
                manday_dict = group_dict.get(group)
                if not (manday_dict["id"] or manday_dict["days"] or manday_dict["precondition"]
                        or manday_dict["status"] or manday_dict["comment"]):
                    continue
                if manday_dict.get("days") == '':
                    manday_dict["days"] = None
                manday_dict[FuncManDay.task_id.name] = task_id
                manday_dict[FuncManDay.option_id.name] = option_id
                manday_dict[FuncManDay.group_id.name] = group_id
                precondition = manday_dict.pop("precondition")
                status = manday_dict.pop("status")
                if manday_dict.get("id"):
                    old_manday_dict = self.get_old_data(FuncManDay, FuncManDay.id, manday_dict.get("id"))[0]
                else:
                    old_manday_dict = None
                    if not status:
                        status = "新建"  # 新增时状态没有时，默认为新建
                issue_status = manday_dict.pop("issue_status")
                manday_dict[FuncManDay.pre_id.name] = self.get_pre_id(precondition, proj_id)
                manday_dict[FuncManDay.status_id.name] = self.get_status_id(status)
                # old_manday_df = manday_df[manday_df["id"] == manday_dict.get("id")]
                # old_manday_dict = old_manday_df.to_dict(orient='records')
                action = self.diff_cost(manday_dict, old_manday_dict)
                if action == "same":
                    continue
                elif action == "add":
                    manday_dict[FuncManDay.create_time.name] = update_time
                    manday_dict[FuncManDay.update_time.name] = update_time
                    manday_dict[FuncManDay.create_user.name] = commit_user
                    manday_dict[FuncManDay.update_user.name] = commit_user
                    manday_dict[FuncManDay.version.name] = 1
                    manday_dict[FuncManDay.base_id.name] = None
                elif action == "change":
                    manday_dict[FuncManDay.update_time.name] = update_time
                    manday_dict[FuncManDay.update_user.name] = commit_user
                    manday_dict[FuncManDay.version.name] = self.update_version(old_manday_dict.get("version"))
                    manday_dict[FuncManDay.base_id.name] = old_manday_dict.get(FuncManDay.base_id.name)
                    manday_dict.pop(FuncManDay.id.name)
                log_dict = self.common_add(self.db_object, manday_dict, None, self.col_list,
                                           self.key_col)
                if log_dict:
                    if action == "add":
                        new_manday = (db.session.query(FuncManDay)
                                      .filter(FuncManDay.id == log_dict.get("key_id"))
                                      .first())
                        # 新增时把base_id设为当前的主键id
                        new_manday.base_id = log_dict.get("key_id")
                    commit_list.append(log_dict)
        return commit_list

    def diff_cost(self, new_data, old_data):
        """
        对比工数信息
        :param old_data:
        :param new_data:
        :return:
        """
        if not old_data:
            action = "add"
            return action
        action = "same"
        for key in self.col_list:
            old_content = old_data.get(key)
            new_content = new_data.get(key)
            if old_content is None:
                old_content = ""
            if new_content is None:
                new_content = ""
            if str(old_content) != str(new_content):
                action = "change"
                break
        return action

    def get_task_cost_history(self, task_id):
        """获取单条task的工数变化信息"""
        try:
            q = (db.session.query(FuncManDay.days, FuncManDay.comment,
                                  Users.user_name, FuncManDay.update_time,
                                  Group.group_name, OptionCombination.value,
                                  Preconditions.precondition)
                 .outerjoin(Users, FuncManDay.update_user == Users.user_id)
                 .outerjoin(Group, FuncManDay.group_id == Group.group_id)
                 .outerjoin(OptionCombination, FuncManDay.option_id == OptionCombination.id)
                 .outerjoin(Preconditions, FuncManDay.pre_id == Preconditions.pre_id)
                 .filter(FuncManDay.task_id == task_id)
                 .order_by(Group.group_name, OptionCombination.value))
            task_history_list = []
            for q_obj in q:
                task_history_dict = dict()
                task_history_dict[FuncManDay.days.name] = q_obj[0]
                task_history_dict[FuncManDay.comment.name] = q_obj[1]
                task_history_dict[FuncManDay.update_user.name] = q_obj[2]
                task_history_dict[FuncManDay.update_time.name] = self.time_to_str(q_obj[3])
                task_history_dict[Group.group_name.name] = q_obj[4]
                task_history_dict["option"] = q_obj[5]
                task_history_dict[Preconditions.precondition.name] = q_obj[6]
                task_history_list.append(task_history_dict)
            return True, task_history_list
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % e)
            return False, "服务异常！请联系管理员！"

    def summary_days_by_option(self, option_list, option_summary_dict):
        option_summary_days = dict()
        for option in option_list:
            option_name = option.get("option_name")
            option_id = option.get("option_id")
            summary_days = option_summary_dict.get(option_id)
            if not summary_days:
                option_summary_days[option_name] = {"days": None}
            else:
                option_summary_days[option_name] = summary_days
        option_summary_days["category_name"] = "工数汇总"
        return option_summary_days

    def summary_cost(self, quotation_id, user_id):
        """工数汇总"""
        role_list = CtrlUser().get_user_roles(user_id)
        if "SALES" not in role_list:
            return False, "您没有权限查看工数汇总！"
        q_obj = self.get_quotation_by_id(quotation_id)
        result = dict()
        if q_obj:
            proj_id = q_obj.proj_id
            quotation_name = q_obj.quotation_name
            quotation_ver = q_obj.quotation_ver
            proj_obj = q_obj.projects
            proj_name = proj_obj.insideName.inside_name
            cost_list = ["days", "precondition", "comment", "status"]
            data_list = []
            option_list, option_ids = self.get_option_list(quotation_id)
            option_name_list = [option.get("option_name") for option in option_list]
            obj_quotation = get_ds_quotation(quotation_id)
            summary_manday_df_dict, option_summary_dict = obj_quotation.summary_manday_by_func(option_ids, proj_id)
            option_summary_days = self.summary_days_by_option(option_list, option_summary_dict)
            func_df = obj_quotation.get_func_df()
            # manday_func_summary_df.reset_index(Functions.func_id.name, inplace=True)
            # func_df = pd.merge(func_df, manday_func_summary_df,
            #                    left_on=Functions.func_id.name,
            #                    right_on=Functions.func_id.name,
            #                    how='left') # 行工数统计
            func_df = func_df.fillna('')
            for i in range(len(func_df)):
                func_dict = func_df.iloc[i].to_dict()
                self.to_int(func_dict)
                func_dict.update(self._summary_cost(option_list, summary_manday_df_dict, i))
                data_list.append(func_dict)
            data_list.append(option_summary_days)
            result["cost_list"] = cost_list
            result["data_list"] = data_list
            result["option_list"] = option_name_list
            # result["option_summary_days"] = option_summary_days
            result["proj_name"] = proj_name
            result["quotation_name"] = quotation_name
            result["quotation_ver"] = quotation_ver
            result["func_task_list"] = obj_quotation.get_func_columns()
            return result, ""
        else:
            return False, "该报价不存在！"

    def _summary_cost(self, option_list, summary_manday_df_dict, i):
        summary_dict = dict()
        for option in option_list:
            option_id = option.get("option_id")
            option_name = option.get("option_name")
            summary_manday_df = summary_manday_df_dict.get(option_id)
            if summary_manday_df is not None:
                s = summary_manday_df.iloc[i]
                s_dict = s.to_dict()
                self.to_int(s_dict)
                summary_dict[option_name] = self.option_summary_cost(s_dict)
            else:
                summary_dict[option_name] = {"days": None,
                                             "precondition": None,
                                             "comment": None,
                                             "status": None
                                             }
        return summary_dict

    def option_summary_cost(self, summary_dict):
        option_summary_dict = dict()
        days = summary_dict.get("days")
        group_list = summary_dict.get("group_name")
        parent_group_list = summary_dict.get("parent_group_name")
        precondition_list = summary_dict.get("precondition")
        comment_list = summary_dict.get("comment")
        status_list = summary_dict.get("status")
        option_summary_dict["days"] = days
        count_group_list = []
        for i, group_name in enumerate(group_list):
            if parent_group_list[i]:
                count_group_list.append(parent_group_list[i])
            else:
                count_group_list.append(group_list[i])
        if count_group_list:
            # self.sgl_replace_gl(group_list)
            group_precondition = []
            group_comment = []
            group_status = []
            for i, precondition in enumerate(precondition_list):
                if precondition is None:
                    precondition = ''
                if precondition:
                    group_precondition.append("%s: %s" % (count_group_list[i], precondition))
            for i, comment in enumerate(comment_list):
                if comment is None:
                    comment = ''
                if comment:
                    group_comment.append("%s: %s" % (count_group_list[i], comment))
            for i, status in enumerate(status_list):
                if status is None:
                    status = ''
                if status:
                    group_status.append("%s: %s" % (count_group_list[i], status))
            status_percent_list = []
            for group in set(count_group_list):
                count1 = group_status.count("%s: %s" % (group, "新建"))
                count2 = group_status.count("%s: %s" % (group, "处理中"))
                count3 = group_status.count("%s: %s" % (group, "确认中"))
                status_percent_list.append("%s: %s" % (group, str(count1+count2+count3)+'/'+str(len(group_list))))
            option_summary_dict["precondition"] = "\n".join(group_precondition)
            option_summary_dict['comment'] = "\n".join(group_comment)
            option_summary_dict["status"] = "\n".join(status_percent_list)
        else:
            option_summary_dict["precondition"] = None
            option_summary_dict["comment"] = None
            option_summary_dict["status"] = None
        return option_summary_dict

    def get_detail_cost(self, func_id):
        """
        获取一条function的详细工数
        :param func_id:
        :return:
        """
        result = dict()
        try:
            func_q = db.session.query(Functions).filter(Functions.func_id == func_id).first()
            if not func_q:
                return False, "func_id:%s不存在！" % func_id
            quotation_id = func_q.quotation_id
            q_obj = self.get_quotation_by_id(quotation_id)
            proj_id = q_obj.proj_id
            option_list, option_ids = self.get_option_list(quotation_id)
            option_name_list = [option.get("option_name") for option in option_list]
            cost_list = ["days", "precondition", "comment", "status"]
            data_list = []
            obj_quotation = get_ds_quotation(quotation_id)
            func_task_df, manday_dict, option_group_ids = obj_quotation.func_manday_detail(option_ids, func_id)
            option_group, group_name_list = self.install_option_group(option_list, option_name_list, option_group_ids)
            func_task_merge_group = self.func_task_merge_group(func_task_df, proj_id)
            func_task_merge_group = func_task_merge_group.fillna('')
            for i in range(len(func_task_merge_group)):
                func_task_dict = func_task_merge_group.iloc[i].to_dict()
                self.to_int(func_task_dict)
                group_name = func_task_dict.get("group_name")
                sgl_group_name = func_task_dict.get("parent_group_name")
                if sgl_group_name:
                    func_task_dict["group_name_list"] = [sgl_group_name, group_name]
                else:
                    func_task_dict["group_name_list"] = [group_name]
                # func_task_dict = self.find_children_group([func_task_dict])[0]
                cost_dict = self.get_cost_data(option_group, manday_dict, i)
                func_task_dict.update(cost_dict)
                data_list.append(func_task_dict)
            result["cost_list"] = cost_list
            result["data_list"] = data_list
            result["option_list"] = option_name_list
            result["group_list"] = group_name_list
            # TODO 有过滤条件时把实际返回的Feature/Task DataFrame作为参数传进来
            result["func_task_list"] = obj_quotation.get_task_columns(func_task_df)
            return True, result
        except Exception as e:
            current_app.logger.error('%s' % e)
            return False, "服务异常！请联系管理员！"

    def install_option_group(self, option_list, option_name_list, option_group_ids):
        group_df = get_group_df()
        group_name_list = []
        option_group = []
        for option in option_list:
            option_id = option.get("option_id")
            option_name = option.get("option_name")
            index = option_list.index(option)
            group_ids = option_group_ids[index]
            if not group_ids:
                option_name_list.remove(option_name)
                continue
            filter_group_df = group_df[group_df["group_id"].isin(group_ids)]
            # ## Option下的组按名称排序
            filter_group_df.sort_values(by=Group.group_name.name, inplace=True)
            group_names = list(filter_group_df[Group.group_name.name])
            group_name_list.append(group_names)
            for i, row in filter_group_df.iterrows():
                group_id = row[Group.group_id.name]
                group_name = row[Group.group_name.name]
                option_group.append(((option_id, group_id), (option_name, group_name)))
            # for i in range(len(group_ids)):
            #     group_id = group_ids[i]
            #     group_name = group_names[i]
            #     option_group.append(((option_id, group_id), (option_name, group_name)))
        return option_group, group_name_list

    def get_cost_summary_info(self, quotation_id, user_id):
        summay_info = self.summary_cost(quotation_id, user_id)
        return summay_info

    def ExcelProduce(self, summay_info, unit='month'):
        option_list_value = summay_info[0]['option_list']
        func_task_list_value = summay_info[0]['func_task_list']+["describe"]
        cost_list_value = summay_info[0]['cost_list']
        data_list_value = summay_info[0]['data_list']
        proj_name = summay_info[0]['proj_name']
        quotation_name = summay_info[0]['quotation_name']
        quotation_ver = summay_info[0]['quotation_ver']
        if not os.path.exists('download'):
            os.mkdir('download')
        now = datetime.datetime.now()
        now_str = now.strftime('%Y-%m-%d_%H-%M-%S-%f')
        cost_summary_path = os.path.join('download', '%s_%s_%s_%s.xlsx' % (proj_name, quotation_name, quotation_ver, now_str))
        workbook = xlsxwriter.Workbook(cost_summary_path)
        worksheet = workbook.add_worksheet()
        cell_format = workbook.add_format({'fg_color': '#A9CCE3', 'border': 1, 'top': 2})
        cell_format2 = workbook.add_format({'fg_color': '#A9CCE3',  'bottom': 2, 'border': 1})

        worksheet.write(2, 0, "Item and Scope", cell_format)
        worksheet.write(3, 0, "category", cell_format2)
        for i in range(1, len(func_task_list_value) + 1):
            worksheet.write(2, i, '', cell_format)

        col = len(func_task_list_value) + 1
        for item in (option_list_value):
            worksheet.write(2, col, item)
            col = col + 4

        col = 1
        for item in (func_task_list_value):
            if item == "describe":
                worksheet.write(3, col, "comment", cell_format2)
            else:
                worksheet.write(3, col, item, cell_format2)
            col = col + 1

        col = len(func_task_list_value) +1
        cell_format = workbook.add_format({'fg_color': '#FAE5D3',  'border': 1,  'bottom': 2})
        len1 = len(option_list_value)
        for i in range(0, len1):
            for value in (cost_list_value):
                if value == "days":
                    if unit == "day":
                        worksheet.write(3, col, "cost(人/日)", cell_format)
                    elif unit == "month":
                        worksheet.write(3, col, "cost(人/月)", cell_format)
                else:
                    worksheet.write(3, col, value, cell_format)
                col = col + 1

        row = 4
        cell_format = workbook.add_format({'text_wrap': 1, 'num_format': '@'})
        cell_format2 = workbook.add_format({'text_wrap': 1, 'num_format': '@', 'right': 1})
        cell_format1 = workbook.add_format({'align': 'right'})
        cell_format3 = workbook.add_format({'align': 'right', 'bottom': 1, 'fg_color': '#FAE5D3'})
        cell_format4 = workbook.add_format({'text_wrap': 1, 'num_format': '@',  'bottom': 1,'fg_color': '#FAE5D3'})
        cell_format5 = workbook.add_format({'text_wrap': 1, 'num_format': '@', 'right': 1, 'bottom': 1, 'fg_color': '#FAE5D3'})
        data_list_len = len(data_list_value)
        option_list_len = len(option_list_value)
        func_len = len(func_task_list_value) + 1
        for index in range(0, data_list_len):
            col = 0
            if data_list_len + 2 >= row:
                for i in range(0, option_list_len):
                    days = data_list_value[index][option_list_value[i]].get('days')
                    if days and unit == "month":
                        days = float(days)/20
                    worksheet.write(row, col + func_len, days, cell_format1)
                    worksheet.write(row, col + func_len + 1, data_list_value[index][option_list_value[i]].get('precondition'), cell_format)
                    worksheet.write(row, col + func_len + 2, data_list_value[index][option_list_value[i]].get('comment'), cell_format)
                    worksheet.write(row, col + func_len + 3, data_list_value[index][option_list_value[i]].get('status'), cell_format2)
                    col = col + 4
            else:
                for i in range(0, option_list_len):
                    days = data_list_value[index][option_list_value[i]].get('days')
                    if days and unit == "month":
                        days = float(days)/20
                    worksheet.write(row, col + func_len, days, cell_format3)
                    worksheet.write(row, col + func_len + 1, data_list_value[index][option_list_value[i]].get('precondition'), cell_format4)
                    worksheet.write(row, col + func_len + 2, data_list_value[index][option_list_value[i]].get('comment'), cell_format4)
                    worksheet.write(row, col + func_len + 3, data_list_value[index][option_list_value[i]].get('status'), cell_format5)
                    col = col + 4
            row = row + 1



        # style config
        merge_format = workbook.add_format({'align': 'center', 'fg_color': '#FAE5D3 ', 'border': 1, 'right': 1, 'top': 2})

        col = len(func_task_list_value) + 1
        for i in range(0, option_list_len):
            worksheet.merge_range(2, col, 2, col + 3, option_list_value[i], merge_format)
            col = col + 4

        index = 1
        cell_format = workbook.add_format({'right': 1, 'text_wrap': 1})
        cell_format1 = workbook.add_format({'right': 1, 'text_wrap': 1, 'bottom': 1, 'fg_color': '#A9CCE3'})
        worksheet.write(index + 3, 0, data_list_value[0]['category_name'], cell_format)
        while index < data_list_len:
            if data_list_len - 1 != index:
                if data_list_value[index]['category_name'] == data_list_value[index - 1]['category_name']:
                    worksheet.write(index + 4, 0, None, cell_format)
                    index = index + 1
                else:
                    worksheet.write(index + 4, 0, data_list_value[index]['category_name'], cell_format)
                    index = index + 1
            else:
                if data_list_value[index]['category_name'] == data_list_value[index - 1]['category_name']:
                    worksheet.write(index + 4, 0, None, cell_format1)
                    index = index + 1

                else:
                    worksheet.write(index + 4, 0, data_list_value[index]['category_name'], cell_format1)
                    index = index + 1

        for i in range(1, len(func_task_list_value) + 1):
            index = 1
            cell_format = workbook.add_format({'right': 1, 'text_wrap': 1})
            cell_format1 = workbook.add_format({'right': 1, 'text_wrap': 1, 'bottom': 1,'fg_color': '#A9CCE3'})
            worksheet.write(index + 3, i, data_list_value[0].get(func_task_list_value[i - 1]), cell_format)
            while index < data_list_len:
                if data_list_len - 1 != index:
                    if data_list_value[index].get(func_task_list_value[i - 1]) == data_list_value[index - 1].get(func_task_list_value[i - 1]):
                        worksheet.write(index + 4, i, None, cell_format)
                        index = index + 1
                    else:
                        worksheet.write(index + 4, i, data_list_value[index].get(func_task_list_value[i - 1]), cell_format)
                        index = index + 1
                else:
                    if data_list_value[index].get(func_task_list_value[i - 1]) == data_list_value[index - 1].get(func_task_list_value[i - 1]):
                        worksheet.write(index + 4, i, None, cell_format1)
                        index = index + 1
                    else:
                        worksheet.write(index + 4, i, data_list_value[index].get(func_task_list_value[i - 1]), cell_format1)
                        index = index + 1

        worksheet.freeze_panes(0, len(func_task_list_value) + 1, 0, len(func_task_list_value) + 1)  # 设置第三列左边固定，右边滚动
        worksheet.set_column(0, 0, 18)  # set Category column width
        worksheet.set_column(1, len(func_task_list_value), 20)  # set function columns width
        workbook.close()
        return cost_summary_path

    def export_cost_summary_info(self, quotation_id, user_id, unit):
        summay_info = self.get_cost_summary_info(quotation_id, user_id)
        data = self.ExcelProduce(summay_info, unit)
        return summay_info, data
