# -*- coding: UTF-8 -*-
import os
import json
import pandas as pd
import numpy as np
from app.ctrl.ctrl_base import CtrlBase
from app.ctrl.ctrl_project import CtrlProject
from app.db.quotations import *
from app.db.projects import *
from app.db.users import *
from app.db.issues import Issue
from app.ctrl.ctrl_user_group import CtrlUserGroup
from flask import current_app
from app.ctrl.utility import Utillity
from app.import_file.import_feature import ImportFeatureList
from app.data_server.ds_quotation import get_ds_quotation
from app.data_server.ds_quotation import refresh_ds_quotation
from app.data_server.ds_pieces import get_group_df, get_gl_sgl_df
from sqlalchemy import func, or_, and_


class CtrlQuotations(CtrlBase):
    def __init__(self):
        CtrlBase.__init__(self)

    def get_base_quotation_list(self, proj_id):
        try:
            q = (db.session.query(Quotations)
                 .filter(Quotations.proj_id == proj_id)
                 .order_by(Quotations.quotation_name)
                 .all())
            res_data = {"qu_list": []}
            for iq in q:
                quoation = dict()
                quoation["base_ver"] = iq.quotation_ver
                quoation["quotation_name"] = iq.quotation_name
                quoation["show_name"] = '/'.join([iq.quotation_name, str(iq.quotation_ver)])
                quoation["quotation_id"] = iq.quotation_id
                res_data["qu_list"].append(quoation)
            return True, res_data
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, str(e)

    def get_all_quotation_list(self):
        try:
            q = (db.session.query(Quotations)
                 .order_by(Quotations.quotation_name, Quotations.update_time.desc())
                 .all())
            res_data = {"quotation_list": []}
            for i_q in q:
                quotation = dict()
                quotation["quotation_id"] = i_q.quotation_id
                quotation["proj_id"] = i_q.proj_id
                quotation["proj_name"] = i_q.projects.insideName.inside_name
                quotation["quotation_name"] = i_q.quotation_name
                quotation["destribe"] = i_q.destribe
                quotation["create_time"] = self.time_to_str(i_q.create_time)
                quotation["update_time"] = self.time_to_str(i_q.update_time)
                quotation["create_user"] = self.get_user_name_by_id(i_q.create_user)
                quotation["update_user"] = self.get_user_name_by_id(i_q.update_user)
                if i_q.status == "2":
                    quotation["status"] = {"status_en": 2, "status_cn": "进行中"}
                else:
                    quotation["status"] = {"status_en": 1, "status_cn": "新建"}
                quotation["quotation_ver"] = i_q.quotation_ver
                quotation["count_issue"] = self.issue_task([], i_q.quotation_id)
                count_not_assign = self.not_assign_function_sales(i_q.quotation_id)
                quotation["count_not_assign"] = count_not_assign
                res_data["quotation_list"].append(quotation)
            return True, res_data
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, str(e)

    def get_all_quotation_list_by_page(self, page, size):
        try:
            q = (db.session.query(Quotations)
                 .order_by(Quotations.quotation_name, Quotations.update_time.desc()))
            count = q.count()
            new_q = list(q.limit(size).offset(size * (page - 1)))
            res_data = {"quotation_list": []}
            for i_q in new_q:
                if not i_q.status == "0":
                    quotation = dict()
                    quotation["quotation_id"] = i_q.quotation_id
                    quotation["proj_id"] = i_q.proj_id
                    quotation["proj_name"] = i_q.projects.insideName.inside_name
                    quotation["quotation_name"] = i_q.quotation_name
                    quotation["destribe"] = i_q.destribe
                    quotation["create_time"] = self.time_to_str(i_q.create_time)
                    quotation["update_time"] = self.time_to_str(i_q.update_time)
                    quotation["create_user"] = self.get_user_name_by_id(i_q.create_user)
                    quotation["update_user"] = self.get_user_name_by_id(i_q.update_user)
                    if i_q.status == "2":
                        quotation["status"] = {"status_en": 2, "status_cn": "进行中"}
                    else:
                        quotation["status"] = {"status_en": 1, "status_cn": "新建"}
                    quotation["quotation_ver"] = i_q.quotation_ver
                    quotation["count_issue"] = self.issue_task([], i_q.quotation_id)
                    count_not_assign = self.not_assign_function_sales(i_q.quotation_id)
                    quotation["count_not_assign"] = count_not_assign
                    res_data["quotation_list"].append(quotation)
            res_data["count"] = count
            return True, res_data
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, str(e)

    def get_base_quotation_list2(self, proj_id):
        try:
            q = (db.session.query(Quotations)
                 .filter(Quotations.parent_quotation_id == 0)
                 .filter(Quotations.proj_id == proj_id)
                 .order_by(Quotations.quotation_id).all())
            res_data = {"qu_list": [], "resource_list": []}
            for fq in q:
                quo = (db.session.query(Quotations)
                       .filter(Quotations.parent_quotation_id == fq.quotation_id)
                       .order_by(Quotations.quotation_id).all())
                quoation = dict()
                quoation["label"] = fq.quotation_name
                quoation["value"] = fq.quotation_id
                quoation["children"] = []
                for iq in quo:
                    children = dict()
                    children["label"] = iq.quotation_name
                    children["value"] = iq.quotation_id
                    children["quotation_resource"] = []
                    RQ = (db.session.query(ResourceQuotation)
                          .filter(ResourceQuotation.quotation_id == iq.quotation_id)
                          .all())
                    for re in RQ:
                        res_checked = dict()
                        res_checked["res_name"] = (db.session.query(InputResourceInfo)
                                                   .filter(InputResourceInfo.resource_id == re.resource_data.resource_id)
                                                   .first()).file_name
                        res_checked["checked_id"] = re.resource_data.id
                        children["quotation_resource"].append(res_checked)
                    quoation["children"].append(children)
                res_data["qu_list"].append(quoation)
            for i_re in (db.session.query(InputResourceInfo)
                         .filter(InputResourceInfo.proj_id == proj_id)
                         .filter(InputResourceInfo.status == '1')
                         .all()):
                resource = dict()
                resource["res_name"] = i_re.file_name
                resource["ver_list"] = []
                for ver in (db.session.query(InputResourceData)
                            .filter(InputResourceData.resource_id == i_re.resource_id)
                            .all()):
                    resource["ver_list"].append({
                        "id": ver.id,
                        "ver": ver.version_id,
                    })
                res_data["resource_list"].append(resource)
            return True, res_data
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, str(e)

    def get_all_precondition(self, proj_id):
        precondition_list = []
        q = db.session.query(Preconditions).filter(Preconditions.proj_id == proj_id).all()
        for pre in q:
            precondition_list.append(pre.precondition)
        return precondition_list

    def get_all_status(self):
        status_list = []
        q = db.session.query(FuncStatus)
        for status in q:
            status_list.append(status.status)
        return status_list

    def get_status_id(self, status):
        q = db.session.query(FuncStatus).filter(FuncStatus.status == status).first()
        if q:
            return q.status_id
        else:
            return None

    def get_pre_id(self, precondition, proj_id):
        q = (db.session.query(Preconditions)
             .filter(Preconditions.precondition == precondition)
             .filter(Preconditions.proj_id == proj_id).first())
        if q:
            return q.pre_id
        else:
            return None

    def get_option_id(self, option_name, quotation_id):
        q = (db.session.query(OptionCombination)
             .filter(OptionCombination.value == option_name)
             .filter(OptionCombination.quotation_id == quotation_id)
             .first())
        if q:
            return q.id
        else:
            return None

    def add_new_precondition(self, precondition_list, proj_id, quotation_id):
        """
        增加新的前提
        :param precondition_list:
        :param proj_id:
        :param quotation_id:
        :return:
        """
        for precondition in precondition_list:
            pre = (db.session.query(Preconditions)
                   .filter(Preconditions.precondition == precondition)
                   .filter(Preconditions.proj_id == proj_id).all())
            if not pre:
                pre_dict = {Preconditions.proj_id.name: proj_id,
                            Preconditions.quotation_id.name: quotation_id,
                            Preconditions.precondition.name: precondition,
                            # Preconditions.create_time.name: self.get_current_time(),
                            # Preconditions.update_time.name: self.get_current_time(),
                            }
                pre_model = Preconditions(**pre_dict)
                db.session.add(pre_model)

    def add_quotation(self, request_data):
        try:
            if ((request_data.get('base_id') == "0") or (request_data.get('base_id') == "undefined")):
                if not request_data.get("file_url"):
                    return False, '请选择上传文件!'
                else:
                    success, msg = self.new_add(request_data)
                    return success, msg
            else:
                if not request_data.get("file_url"):
                    success, msg = self.extend_add(request_data)
                    return success, msg
                else:
                    success, msg = self.new_add(request_data)
                    return success, msg

        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"

    def new_add(self, request_data):
        file_url = request_data.get("file_url")
        commiter = request_data.get('commit_user')
        proj_id = request_data.get('proj_id')
        destribe = request_data.get('describe')
        quotation_name = request_data.get('quotation_name')
        base_id = request_data.get('base_id')
        if not db.session.query(Projects).filter(Projects.proj_id == proj_id).first():
            return False, '没有此项目!'
        if (base_id == 0) or (base_id == "undefined"):
            base_quotation_id = None
        else:
            base_quotation_id = base_id
        quotation_id = self.add_quotation_to_teble(proj_id, base_quotation_id, destribe, quotation_name, commiter)
        tree_list = ImportFeatureList().get_feature_tree3(file_url)
        sub_name_list = ImportFeatureList().get_features(tree_list)
        success, msg = self.get_onerow_info3(sub_name_list, proj_id, quotation_id, commiter)
        if not success:
            return False, msg
        default_option = {OptionCombination.quotation_id.name: quotation_id,
                          OptionCombination.value.name: "Default",
                          OptionCombination.checked.name: True,
                          }
        db.session.add(OptionCombination(**default_option))
        db.session.commit()
        refresh_ds_quotation(quotation_id)
        return True, quotation_id

    def import_featurelist(self, request_data):
        try:
            file_upload = request_data.files['file']
            file_name = file_upload.filename
            uti = Utillity()
            only_id = uti.get_nextval("file_seq_file_id_seq")
            file_path = os.path.abspath(os.path.join(os.getcwd(), r'data', r'temp', str(only_id)))
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            file_upload.save(os.path.join(file_path, file_name))
            file = dict()
            file["file_name"] = file_name
            file["file_url"] = os.path.join(file_path, file_name)
            return True, file
        except Exception as e:
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"

    def extend_add(self, request_data):
        commiter = request_data.get('commit_user')
        proj_id = request_data.get('proj_id')
        destribe = request_data.get('describe')
        quotation_name = request_data.get('quotation_name')
        base_id = request_data.get('base_id')
        if not db.session.query(Projects).filter(Projects.proj_id == proj_id).first():
            return False, '没有此项目!'
        if (base_id == 0) or (base_id == "undefined"):
            base_quotation_id = None
        else:
            base_quotation_id = base_id
        quotation_id = self.add_quotation_to_teble(proj_id, base_quotation_id, destribe,
                                                    quotation_name, commiter)
        self.add_func_by_extend3(base_id, quotation_id, commiter)
        db.session.commit()
        refresh_ds_quotation(quotation_id)
        return True, quotation_id

    def find_name_repeat(self, name):
        q = db.session.query(Quotations).filter(Quotations.quotation_name == name).all()
        if q:
            return True
        else:
            return False

    def add_func_by_extend(self, base_id, quotation_id, commiter):
        """
        需继承combination
        :param base_id:
        :param quotation_id:
        :param commiter:
        :return:
        """
        funcs = (db.session.query(Functions)
                 .filter(Functions.quotation_id == base_id)
                 .order_by(Functions.order_id).all())
        comb_dict = self.add_option_by_extend(base_id, quotation_id)
        for i_func in funcs:
            name_info = self.get_name_list_by_id(i_func)
            category_name = i_func.category.category_name
            describe = i_func.describe
            order_id = i_func.order_id
            base_func_id = i_func.func_id
            func_id = self.add_info_to_functable(name_info, category_name, describe,
                                                 quotation_id, commiter, order_id, base_func_id)
            self.add_func_group_by_extend(base_func_id, func_id)
            self.add_task_by_extend(base_func_id, func_id, commiter, comb_dict)

    def add_func_by_extend3(self, base_id, quotation_id, commiter):
        """
        需继承combination
        :param base_id:
        :param quotation_id:
        :param commiter:
        :return:
        """
        funcs = (db.session.query(Functions)
                 .filter(Functions.quotation_id == base_id)
                 .order_by(Functions.order_id).all())
        comb_dict = self.add_combination_by_extend3(base_id, quotation_id)
        for i_func in funcs:
            name_info = self.get_name_list_by_id(i_func)
            category_name = i_func.category.category_name
            describe = i_func.describe
            order_id = i_func.order_id
            base_func_id = i_func.func_id
            func_id = self.add_info_to_functable(name_info, category_name, describe,
                                                 quotation_id, commiter, order_id, base_func_id)
            self.add_func_group_by_extend(base_func_id, func_id)
            self.add_task_by_extend(base_func_id, func_id, commiter, comb_dict)

    def add_func_group_by_extend(self, old_func_id, new_func_id):
        q = (db.session.query(FuncGroup)
             .filter(FuncGroup.func_id == old_func_id)
             .order_by(FuncGroup.id).all())
        for ifg in q:
            fg = FuncGroup()
            fg.func_id = new_func_id
            fg.group_id = ifg.group_id
            db.session.add(fg)

    def add_func_by_extend2(self, base_id, quotation_id, commiter):
        """
        先不继承combination
        :param base_id:
        :param quotation_id:
        :param commiter:
        :return:
        """
        funcs = (db.session.query(Functions)
                 .filter(Functions.quotation_id == base_id)
                 .order_by(Functions.order_id).all())
        # TODO @zhangkairan 目前不需要继承combination 需要时候再打开
        # comb_dict = self.add_option_by_extend(base_id)
        self.add_option_by_extend(base_id)
        for i_func in funcs:
            name_info = self.get_name_list_by_id(i_func)
            category_name = i_func.category.category_name
            describe = i_func.describe
            order_id = i_func.order_id
            base_id = i_func.func_id
            func_id = self.add_info_to_functable(name_info, category_name, describe,
                                                 quotation_id, commiter, order_id, base_id)
            self.add_task_by_extend2(base_id, func_id, commiter)
        # ## TODO@hcz: temp
        comb = OptionCombination()
        comb.value = 'default'
        comb.quotation_id = quotation_id
        db.session.add(comb)

    def add_option_by_extend(self, base_id, quotation_id):
        options = (db.session.query(Options)
                   .filter(Options.quotation_id == base_id)
                   )
        old_new_dict = {}
        for op in options:
            op_id = self.extend_option_to_table(op, quotation_id)
            old_new_dict = self.extend_option_value_to_table(op_id, op, old_new_dict)
        comb_old_new_dict = self.add_combination_by_extend(base_id, quotation_id, old_new_dict)
        return comb_old_new_dict

    def add_option_by_extend2(self, quotation_id):
        """
        不继承combination
        :param quotation_id:
        :return:
        """
        options = (db.session.query(Options)
                   .filter(Options.quotation_id == quotation_id)
                   )
        old_new_dict = {}
        for op in options:
            op_id = self.extend_option_to_table(op, quotation_id)
            old_new_dict = self.extend_option_value_to_table(op_id, op, old_new_dict)
        # comb_old_new_dict = self.add_combination_by_extend(quotation_id, old_new_dict)
        # return comb_old_new_dict

    def add_combination_by_extend(self, base_id, quotation_id, value_dict):
        """
        :param base_id: 被继承的项目ID
        :param quotation_id: 新项目ID
        :param value_dict:
        :return:
        """
        combs = (db.session.query(OptionCombination)
                 .filter(OptionCombination.quotation_id == base_id)
                 .all())
        old_new_cict = {}
        if combs:
            for i_comb in combs:
                old_new_cict = self.extend_combination_to_table(quotation_id, i_comb, value_dict, old_new_cict)
        return old_new_cict

    def add_combination_by_extend3(self, base_id, quotation_id):
        """
        :param base_id: 被继承的项目ID
        :param quotation_id: 新项目ID
        :return:
        """
        combs = (db.session.query(OptionCombination)
                 .filter(OptionCombination.quotation_id == base_id)
                 .all())
        old_new_dict = {}
        if combs:
            for i_comb in combs:
                old_new_dict = self.extend_combination_to_table3(quotation_id, i_comb, old_new_dict)
        return old_new_dict

    def extend_combination_to_table3(self, quotation_id, info, old_new_dict):
        # 将info的id和新ID作成dict，方便工数表继承
        combination_info = {
            OptionCombination.quotation_id.name: quotation_id,
            OptionCombination.proj_id.name: info.proj_id,
            OptionCombination.checked.name: info.checked,
            OptionCombination.value.name: info.value,
        }
        combination = OptionCombination(**combination_info)
        db.session.add(combination)
        db.session.flush()
        old_new_dict[info.id] = combination.id
        return old_new_dict

    def extend_combination_to_table(self, quotation_id, info, value_dict, old_new_cict):
        # 将info的option_value_id_list与value_list中old值做对比，将new值替换进去
        new_id = self.replace_option_value(info.option_value_id_list, value_dict)
        combination_info = {
            OptionCombination.quotation_id.name: quotation_id,
            OptionCombination.option_value_id_list.name: new_id,
            OptionCombination.value.name: info.value,
        }
        combination = OptionCombination(**combination_info)
        db.session.add(combination)
        db.session.flush()
        old_new_cict[info.id] = combination.id
        return old_new_cict

    def replace_option_value(self, old_option, old_new_dict):
        if old_option:
            new_options = []
            old_options = old_option.split(',')
            for old in old_options:
                new = old_new_dict.get(int(old))
                if not new:
                    raise Exception('error')
                new_options.append(str(new))
            return ','.join(new_options)
        else:
            return ''

    def extend_option_to_table(self, info, quotation_id):
        option_info = {
            Options.quotation_id.name: quotation_id,
            Options.proj_id.name: info.proj_id,
            Options.option_name.name: info.option_name,
            Options.create_time.name: self.get_current_time(),
            Options.update_time.name: self.get_current_time(),
        }
        option = Options(**option_info)
        db.session.add(option)
        db.session.flush()
        return option.option_id

    def extend_option_value_to_table(self, op_id, info, old_new_dict):
        for i_value in info.option_value:
            value_info = {
                OptionValue.option_id.name: op_id,
                OptionValue.option_value.name: i_value.option_value,
            }
            value = OptionValue(**value_info)
            db.session.add(value)
            db.session.flush()
            old_new_dict[i_value.value_id] = value.value_id
        return old_new_dict

    # def add_func_by_extend(self, parent_quotation_id, quotation_id, commiter):
    #     funcs = (db.session.query(Functions)
    #              .filter(Functions.quotation_id == parent_quotation_id)
    #              .order_by().all())
    #     for i_func in funcs:
    #         name_info = self.get_name_list_by_id(i_func)
    #         category_name = i_func.category.category_name
    #         describe = i_func.describe
    #         order_id = i_func.order_id
    #         base_id = i_func.func_id
    #         func_id = self.add_info_to_functable(name_info, category_name, describe,
    #                                              quotation_id, commiter, order_id, base_id)
    #         self.add_task_by_extend(func_id, commiter)

    def get_name_list_by_id(self, func_info):
        name_info = {
            "sub1": func_info.sub1,
            "sub2": func_info.sub2,
            "sub3": func_info.sub3,
            "sub4": func_info.sub4,
            "sub5": func_info.sub5,
            "sub6": func_info.sub6,
            "sub7": func_info.sub7,
            "sub8": func_info.sub8,
            "sub9": func_info.sub9,
            "sub10": func_info.sub10,
        }
        return name_info

    def add_task_by_extend(self, base_id, func_id, commiter, comb_dict):
        task_list = db.session.query(Task).filter(Task.func_id == base_id).order_by().all()
        for i_task in task_list:
            task_id = self.extend_task_to_table(i_task, func_id, commiter)
            fun_man_day = (db.session.query(FuncManDay)
                           .filter(FuncManDay.task_id == i_task.task_id)
                           .first())
            if fun_man_day:
                self.extend_fun_man_day(task_id, fun_man_day, commiter, comb_dict)

    def add_task_by_extend2(self, base_id, func_id, commiter):
        task_list = db.session.query(Task).filter(Task.func_id == base_id).order_by().all()
        for i_task in task_list:
            task_id = self.extend_task_to_table(i_task, func_id, commiter)
            fun_man_day = (db.session.query(FuncManDay)
                           .filter(FuncManDay.task_id == i_task.task_id)
                           .first())
            if fun_man_day:
                self.extend_fun_man_day2(task_id, fun_man_day, commiter)

    def get_task_name_list_by_id(self, task_info):
        task_info = {
            "task1": task_info.sub1,
            "task2": task_info.sub2,
            "task3": task_info.sub3,
            "task4": task_info.sub4,
            "task5": task_info.sub5,
            "task6": task_info.sub6,
        }
        return task_info

    def extend_task_to_table(self, task_info, func_id, commiter):
        tree_info = {
            Task.func_id.name: func_id,
            Task.task_version.name: 0,               # 0当前最新版本
            Task.update_time.name: self.get_current_time(),
            Task.create_time.name: self.get_current_time(),
            Task.create_user.name: commiter,
            Task.update_user.name: commiter,
            # Task.describe.name: task_info.describe,
            Task.group_id.name: task_info.group_id,
            Task.order_id.name: task_info.order_id,
            Task.task1.name: task_info.task1,
            Task.task2.name: task_info.task2,
            Task.task3.name: task_info.task3,
            Task.task4.name: task_info.task4,
            Task.task5.name: task_info.task5,
            Task.task6.name: task_info.task6,
        }
        tree = Task(**tree_info)
        db.session.add(tree)
        db.session.flush()
        return tree.task_id

    def get_onerow_info3(self, tree_list, proj_id, quotation_id, commiter):
        """
        将Featurelist文件的树形结构逐条添加
        :param tree_list:
        :param quotation_id:
        :param commiter:
        """
        index = 0
        for item in tree_list:
            index = index + 1
            name_info = {"sub1": None, "sub2": None, "sub3": None, "sub4": None, "sub5": None,
                         "sub6": None, "sub7": None, "sub8": None, "sub9": None, "sub10": None}
            category_name = item[0]["category"]
            describe = item[-1]["comment"]

            for i in range(len(item)):
                name_info["sub{}".format(i+1)] = item[i]["name"]
            func_id = self.add_info_to_functable(name_info, category_name, describe, quotation_id, commiter, index, 0)
            self.add_default_task(func_id, commiter)
        return True, ''

    def get_onerow_info(self, tree_list, proj_id, quotation_id, commiter):
        """
        将Featurelist文件的树形结构逐条添加
        :param tree_list:
        :param quotation_id:
        :param commiter:
        """
        index = 0
        for item in tree_list:
            index = index + 1
            name_info = {"sub1": None, "sub2": None, "sub3": None, "sub4": None, "sub5": None,
                         "sub6": None, "sub7": None, "sub8": None, "sub9": None, "sub10": None}
            category_name = item[0]["category"]
            describe = item[0]["comment"]

            for i in range(len(item)):
                name_info["sub{}".format(i+1)] = item[i]["name"]
            func_id = self.add_info_to_functable(name_info, category_name, describe, quotation_id, commiter, index, 0)
            if item[-1]["group"]:
                group_name = item[-1]["group"]
            elif item[-1]["parent_group"]:
                group_name = item[-1]["parent_group"]
            else:
                group_name = None
            if group_name:
                success, msg = self.find_func_id_in_funcgroup_table(proj_id, group_name, func_id)
                if not success:
                    return False, msg
                group_id = msg
            else:
                group_id = None
            self.add_default_task(func_id, commiter, group_id)
        return True, ''

    def add_default_task(self, func_id, commiter, group_id=None):
        task_info = {
                "func_id": func_id, "describe": None, "group_id": group_id, "order_id": None,
                "task1": None, "task2": None, "task3": None, "task4": None, "task5": None, "task6": None, }
        self.add_task_to_table(task_info, commiter)

    def add_task_to_table(self, task_info, commiter):
        tree_info = {
            Task.func_id.name: task_info.get("func_id"),
            Task.task_version.name: 0,               # 0当前最新版本
            Task.update_time.name: self.get_current_time(),
            Task.create_time.name: self.get_current_time(),
            Task.create_user.name: commiter,
            Task.update_user.name: commiter,
            # Task.describe.name: task_info.get("describe"),
            Task.group_id.name: task_info.get("group_id"),
            Task.order_id.name: task_info.get("order_id"),
            Task.task1.name: task_info.get("task1"),
            Task.task2.name: task_info.get("task2"),
            Task.task3.name: task_info.get("task3"),
            Task.task4.name: task_info.get("task4"),
            Task.task5.name: task_info.get("task5"),
            Task.task6.name: task_info.get("task6"),
        }
        tree = Task(**tree_info)
        db.session.add(tree)

    def add_info_to_functable(self, name_info, category_name, describe, quotation_id, user_id, order_id, base_id):
        """
        增加新的func信息
        """
        cat_id = self.find_cat_and_return(category_name)
        func_info = {
            Functions.category_id.name: cat_id,
            Functions.describe.name: describe,
            Functions.base_func_id.name: base_id,
            Functions.sub1.name: name_info.get("sub1"),
            Functions.sub2.name: name_info.get("sub2"),
            Functions.sub3.name: name_info.get("sub3"),
            Functions.sub4.name: name_info.get("sub4"),
            Functions.sub5.name: name_info.get("sub5"),
            Functions.sub6.name: name_info.get("sub6"),
            Functions.sub7.name: name_info.get("sub7"),
            Functions.sub8.name: name_info.get("sub8"),
            Functions.sub9.name: name_info.get("sub9"),
            Functions.sub10.name: name_info.get("sub10"),
            Functions.quotation_id.name: quotation_id,
            Functions.func_version.name: 0,                            # 0当前最新版本
            Functions.create_time.name: self.get_current_time(),
            Functions.update_time.name: self.get_current_time(),
            Functions.update_user.name: user_id,
            Functions.create_user.name: user_id,
            Functions.order_id.name: order_id,                         # 排序
        }
        fun = Functions(**func_info)
        db.session.add(fun)
        db.session.flush()
        return fun.func_id

    # def add_info_to_functree(self, func_id, parent_func_id, fun_ver, quotation_id, commiter):
    #     """
    #     增加新的functree信息
    #     """
    #     tree_info = {
    #         FuncTree.func_id.name: func_id,
    #         FuncTree.func_version.name: 0,                     # 0当前最新版本
    #         FuncTree.parent_func_id.name: parent_func_id,
    #         FuncTree.parent_func_version.name: fun_ver,
    #         FuncTree.update_user_id.name: commiter,
    #         FuncTree.quotation_id.name: quotation_id,
    #     }
    #     tree = FuncTree(**tree_info)
    #     db.session.add(tree)
    #     # db.session.commit()
    #     db.session.flush()

    def find_cat_and_return(self, cat_name):
        cat = db.session.query(Category).filter(Category.category_name == cat_name).first()
        if cat:
            c_id = cat.category_id
        else:
            c_id = self.add_category(cat_name)
        return c_id

    def add_category(self, category_name):
        cat = Category(category_name=category_name)
        db.session.add(cat)
        # db.session.commit()
        db.session.flush()
        return cat.category_id

    def add_quotation_to_teble(self, proj_id, base_quotation_id, destribe, quotation_name, commiter):
        """
        增加新的quotation
        """
        old_quotation = db.session.query(Quotations).filter(Quotations.quotation_name == quotation_name).all()
        pro_info = {
            Quotations.quotation_ver.name: len(old_quotation)+1,
            Quotations.parent_quotation_id.name: None,
            Quotations.proj_id.name: proj_id,
            Quotations.base_quotation_id.name: base_quotation_id,
            Quotations.quotation_name.name: quotation_name,
            Quotations.destribe.name: destribe,
            Quotations.create_time.name: self.get_current_time(),
            Quotations.update_time.name: self.get_current_time(),
            Quotations.create_user.name: commiter,
            Quotations.update_user.name: commiter,
            Quotations.status.name: 1,                     # 1新建，0为删除(完成已关闭), 2进行中
        }
        pro = Quotations(**pro_info)
        db.session.add(pro)
        db.session.flush()
        return pro.quotation_id

    def get_one_quotation_info(self, quotation_id):
        try:
            qs = db.session.query(Quotations).filter(Quotations.quotation_id == quotation_id).first()
            if qs:
                quotation = dict()
                quotation["quotation_id"] = qs.quotation_id
                quotation["parent_quotation_id"] = qs.parent_quotation_id
                quotation["proj_id"] = qs.proj_id
                quotation["quotation_name"] = qs.quotation_name
                quotation["destribe"] = qs.destribe
                quotation["create_time"] = self.time_to_str(qs.create_time)
                quotation["update_time"] = self.time_to_str(qs.update_time)
                quotation["create_user"] = self.get_user_name_by_id(qs.create_user)
                quotation["update_user"] = self.get_user_name_by_id(qs.update_user)
                if qs.status == "0":
                    quotation["status"] = "已删除"
                else:
                    quotation["status"] = "新建"
                # if not qs.parent_quotation_id == 0:
                #     quotation["parent_quotation_name"] = (db.session.query(Quotations)
                #                                           .filter(Quotations.quotation_id == qs.parent_quotation_id)
                #                                           .first()).quotation_name
                # else:
                #     quotation["parent_quotation_name"] = ""
                return True, quotation
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, str(e)

    def update_one_quotation_info(self, quotation_id, data):
        try:
            q = db.session.query(Quotations).filter(Quotations.quotation_id == quotation_id).all()
            if q:
                if db.session.query(Quotations).filter(Quotations.quotation_name == data.get("quotation_name")).all():
                    return False, "此报价名已存在"
                q[0].quotation_name = data.get("quotation_name")
                q[0].destribe = data.get("destribe")
                q[0].update_time = self.get_current_time()
                q[0].update_user = data.get("user")
                db.session.commit()
                return True, q[0].proj_id
            else:
                return False, "沒有此报价"
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"

    def get_user_name_by_id(self, user_id):
        user = db.session.query(Users).filter(Users.user_id == user_id).first()
        if user:
            return user.user_name
        else:
            return ''

    def extend_fun_man_day(self, task_id, old_man_day, commiter, comb_dict):
        """
        继承之前的fun_man_day信息
        """
        manday_info = {
            FuncManDay.task_id.name: task_id,
            FuncManDay.group_id.name: old_man_day.group_id,
            FuncManDay.option_id.name: comb_dict.get(old_man_day.option_id),
            FuncManDay.pre_id.name: old_man_day.pre_id,
            FuncManDay.assin_to.name: old_man_day.assin_to,
            FuncManDay.status_id.name: old_man_day.status_id,
            FuncManDay.days.name: old_man_day.days,
            FuncManDay.comment.name: old_man_day.comment,
            FuncManDay.create_time.name: self.get_current_time(),
            FuncManDay.update_time.name: self.get_current_time(),
            FuncManDay.create_user.name: commiter,
            FuncManDay.update_user.name: commiter,
        }
        manday = FuncManDay(**manday_info)
        db.session.add(manday)
        # db.session.commit()
        db.session.flush()

    def extend_fun_man_day2(self, task_id, old_man_day, commiter):
        """
        继承之前的fun_man_day信息,此方法不复制op_combination
        """
        manday_info = {
            FuncManDay.task_id.name: task_id,
            FuncManDay.group_id.name: old_man_day.group_id,
            FuncManDay.option_id.name: None,
            FuncManDay.pre_id.name: old_man_day.pre_id,
            FuncManDay.assin_to.name: old_man_day.assin_to,
            FuncManDay.status_id.name: old_man_day.status_id,
            FuncManDay.days.name: old_man_day.days,
            FuncManDay.comment.name: old_man_day.comment,
            FuncManDay.create_time.name: self.get_current_time(),
            FuncManDay.update_time.name: self.get_current_time(),
            FuncManDay.create_user.name: commiter,
            FuncManDay.update_user.name: commiter,
        }
        manday = FuncManDay(**manday_info)
        db.session.add(manday)
        # db.session.commit()
        db.session.flush()

    # def add_fun_man_day(self, task_id, old_task):
    #     """
    #     增加新的fun_man_day信息
    #     """
    #     groups = CtrlUserGroup().get_groups()
    #     for group in groups:
    #         manday_info = {
    #             FuncManDay.func_only_id.name: func_only_id,
    #             FuncManDay.group_id.name: group.get("group_id"),
    #             FuncManDay.option_id.name: None,
    #             FuncManDay.pre_id.name: None,
    #             FuncManDay.assin_to.name: None,
    #             FuncManDay.status_id.name: 1,
    #             FuncManDay.days.name: None,
    #             FuncManDay.comment.name: None,
    #             FuncManDay.create_time.name: self.get_current_time(),
    #             FuncManDay.update_time.name: self.get_current_time(),
    #         }
    #         manday = FuncManDay(**manday_info)
    #         db.session.add(manday)
    #         # db.session.commit()
    #         db.session.flush()

    def get_fun_man_day_by_id(self):
        return

    def get_quotation_list2_by_size(self, proj_id, user_id, page, size):
        try:
            from app.ctrl.ctrl_user import CtrlUser
            role_list = CtrlUser().get_user_roles(user_id)
            role = "GL"
            if "SALES" in role_list:
                role = "SALES"
            elif "SGL" in role_list:
                role = "SGL"
            q = (db.session.query(Quotations)
                 .filter(Quotations.proj_id == proj_id)
                 .order_by(Quotations.update_time.desc()))
            count = q.count()
            new_q = q.limit(size).offset(size * (page - 1))
            content = dict()
            content["quotation_list"] = self.quotations_to_dict(list(new_q), proj_id, user_id, role)
            content["count"] = count

            return True, content
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, str(e)

    def get_quotation_list(self, proj_id):
        try:
            q = (db.session.query(Quotations)
                 .filter(Quotations.proj_id == proj_id)
                 .order_by(Quotations.update_time.desc()).all())
            q_list = []
            for i_q in q:
                if not i_q.status == "0":                              # 查找状态不为0(删除)的
                    quotation = dict()
                    quotation["quotation_id"] = i_q.quotation_id
                    quotation["proj_id"] = i_q.proj_id
                    quotation["proj_name"] = i_q.projects.insideName.inside_name
                    quotation["quotation_name"] = i_q.quotation_name
                    quotation["destribe"] = i_q.destribe
                    quotation["create_time"] = self.time_to_str(i_q.create_time)
                    quotation["update_time"] = self.time_to_str(i_q.update_time)
                    quotation["create_user"] = self.get_user_name_by_id(i_q.create_user)
                    quotation["update_user"] = self.get_user_name_by_id(i_q.update_user)
                    if i_q.status == "2":
                        quotation["status"] = "进行中"
                    else:
                        quotation["status"] = "新建"
                    quotation["quotation_ver"] = i_q.quotation_ver
                    q_list.append(quotation)
            return True, q_list
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, str(e)

    def get_quotation_list_by_user_id_page(self, user_id, page, size):
        try:
            from app.ctrl.ctrl_user import CtrlUser
            role_list = CtrlUser().get_user_roles(user_id)
            role = "GL"
            if "SALES" in role_list:
                role = "SALES"
            elif "SGL" in role_list:
                role = "SGL"
            proj_list = self.get_proj_by_user(user_id)
            proj_id_list = [proj.proj_id for proj in proj_list]
            q = (db.session.query(Quotations)
                 .filter(Quotations.proj_id.in_(proj_id_list))
                 # .filter(Quotations.status == xxx)  # TODO@zhangkairan:
                 .order_by(Quotations.update_time.desc()))
            count = q.count()
            new_q = q.limit(size).offset(size * (page - 1))
            content = dict()
            content["quotation_list"] = self.quotations_to_dict_df(list(new_q), user_id, role)
            content["count"] = count
            return True, content
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, str(e)

    def get_not_del_quotations(self):
        q = (db.session.query(Quotations)
             .filter(Quotations.status == 1)
             .order_by().first())
        return q

    def check_feature_group(self, quotation_id, group_id_list):
        q = (db.session.query(FuncGroup)
             .outerjoin(Functions, Functions.func_id == FuncGroup.func_id)
             .filter(Functions.quotation_id == quotation_id)
             .all())
        for i_feature in q:
            if i_feature.group_id in group_id_list:
                return True
        return False

    def check_task_group(self, quotation_id, group_id_list):
        q = (db.session.query(Task)
             .outerjoin(Functions, Functions.func_id == Task.func_id)
             .filter(Functions.quotation_id == quotation_id)
             .all())
        for i_task in q:
            if i_task.group_id in group_id_list:
                return True
        return False

    def quotations_to_dict(self, quotations, proj_id, user_id, role='GL'):
        q_list = []
        group_list_df = get_gl_sgl_df(proj_id)
        parent_group_id_list = group_list_df["parent_group_id"].tolist()
        group_id_list = self.get_my_and_sub_group_owner_users(user_id)
        group_list, group_ids, parent_sub_group_ids = self.get_group_list_by_df(group_id_list, proj_id, parent_group_id_list)
        parent_group_ids = list(set(parent_sub_group_ids).difference(set(group_ids)))  # 取所有的父组（SGL组）
        for i_q in quotations:
            if not i_q.status == "0":
                quotation = dict()
                quotation["quotation_id"] = i_q.quotation_id
                quotation["proj_id"] = i_q.proj_id
                quotation["proj_name"] = i_q.projects.insideName.inside_name
                quotation["quotation_name"] = i_q.quotation_name
                quotation["destribe"] = i_q.destribe
                quotation["create_time"] = self.time_to_str(i_q.create_time)
                quotation["update_time"] = self.time_to_str(i_q.update_time)
                quotation["create_user"] = self.get_user_name_by_id(i_q.create_user)
                quotation["update_user"] = self.get_user_name_by_id(i_q.update_user)
                if i_q.status == "2":
                    quotation["status"] = "进行中"
                else:
                    quotation["status"] = "新建"
                quotation["quotation_ver"] = i_q.quotation_ver
                # group_list, group_ids, parent_sub_group_ids = self.get_group_list(user_id, i_q.quotation_id)
                # my_group = CtrlUserGroup().get_my_group(user_id, i_q.proj_id)
                # my_group_id = my_group.get("group_id")
                count_issue = self.issue_task(parent_sub_group_ids, i_q.quotation_id)
                quotation["count_issue"] = count_issue
                if role == "SALES":
                    count_not_assign = self.not_assign_function_sales(i_q.quotation_id)
                    quotation["count_not_assign"] = count_not_assign
                elif role == "SGL":
                    count_not_assign = self.not_assign_function_sgl(parent_group_ids, group_ids, i_q.quotation_id)
                    count_not_confirm = self.not_confirm_task_sgl(parent_sub_group_ids, i_q.quotation_id)
                    quotation["count_not_assign"] = count_not_assign
                    quotation["count_not_confirm"] = count_not_confirm
                elif role == "GL":
                    count_not_quotation = self.not_quotation_task_gl(parent_sub_group_ids, i_q.quotation_id)
                    quotation["count_not_quotation"] = count_not_quotation
                q_list.append(quotation)
        return q_list

    def quotations_to_dict_df(self, quotations, user_id, role='GL'):
        q_list = []
        group_id_list = self.get_my_and_sub_group_owner_users(user_id)
        for i_q in quotations:
            if not i_q.status == "0":
                quotation = dict()
                quotation["quotation_id"] = i_q.quotation_id
                quotation["proj_id"] = i_q.proj_id
                quotation["proj_name"] = i_q.projects.insideName.inside_name
                quotation["quotation_name"] = i_q.quotation_name
                quotation["destribe"] = i_q.destribe
                quotation["create_time"] = self.time_to_str(i_q.create_time)
                quotation["update_time"] = self.time_to_str(i_q.update_time)
                quotation["create_user"] = self.get_user_name_by_id(i_q.create_user)
                quotation["update_user"] = self.get_user_name_by_id(i_q.update_user)
                if i_q.status == "2":
                    quotation["status"] = {"status_en": 2, "status_cn": "进行中"}
                else:
                    quotation["status"] = {"status_en": 1, "status_cn": "新建"}
                quotation["quotation_ver"] = i_q.quotation_ver
                group_list_df = get_gl_sgl_df(i_q.proj_id)
                parent_group_id_list = group_list_df["parent_group_id"].tolist()
                group_list, group_ids, parent_sub_group_ids = self.get_group_list_by_df(group_id_list, i_q.proj_id,
                                                                                        parent_group_id_list)
                parent_group_ids = list(set(parent_sub_group_ids).difference(set(group_ids)))  # 取所有的父组（SGL组）
                # my_group = CtrlUserGroup().get_my_group(user_id, i_q.proj_id)
                # my_group_id = my_group.get("group_id")
                count_issue = self.issue_task(parent_sub_group_ids, i_q.quotation_id)
                quotation["count_issue"] = count_issue
                if role == "SALES":
                    count_not_assign = self.not_assign_function_sales(i_q.quotation_id)
                    quotation["count_not_assign"] = count_not_assign
                elif role == "SGL":
                    count_not_assign = self.not_assign_function_sgl(parent_group_ids, group_ids, i_q.quotation_id)
                    count_not_confirm = self.not_confirm_task_sgl(parent_sub_group_ids, i_q.quotation_id)
                    quotation["count_not_assign"] = count_not_assign
                    quotation["count_not_confirm"] = count_not_confirm
                elif role == "GL":
                    count_not_quotation = self.not_quotation_task_gl(parent_sub_group_ids, i_q.quotation_id)
                    quotation["count_not_quotation"] = count_not_quotation
                q_list.append(quotation)
        return q_list

    def get_proj_by_user(self, user_id):
        q = (db.session.query(Projects)
             .outerjoin(UserRole, UserRole.proj_id == Projects.proj_id)
             .filter(UserRole.user_id == user_id)
             .order_by(Projects.proj_id))
        q2 = (db.session.query(Projects)
              .outerjoin(ProjectObserver, ProjectObserver.proj_id == Projects.proj_id)
              .filter(ProjectObserver.observer_id == user_id)
              .order_by(Projects.proj_id))

        proj_list = q.union(q2).all()
        return proj_list

    def get_quotation_by_id(self, quotation_id):
        q = (db.session.query(Quotations)
             .filter(Quotations.quotation_id == quotation_id)
             .order_by().first())
        return q

    # def get_feature_list(self, quotation_id, user_id):
    #     q_obj = self.get_quotation_by_id(quotation_id)
    #     result = {"feature_list": [], "columns": [], "column_num": 0}
    #     if q_obj:
    #         quotation_name = q_obj.quotation_name
    #         quotation_ver = q_obj.quotation_ver
    #         proj_obj = q_obj.projects
    #         proj_name = proj_obj.insideName.inside_name
    #         proj_id = proj_obj.proj_id
    #         # my_group = CtrlUserGroup().get_my_group(user_id, proj_id)
    #         obj_quotation = get_ds_quotation(quotation_id)
    #         func_df = obj_quotation.get_func_df()
    #         func_group_df = obj_quotation.get_func_group_df()
    #         merged_func_df = obj_quotation.merge_func_group_id(func_df, func_group_df)
    #         func_list = self.load_func_cats(func_df, merged_func_df)
    #         # func_list = merged_func_df.to_dict(orient="records")
    #         # result["my_group"] = my_group.get("group_name")
    #         result["proj_id"] = proj_id
    #         result["proj_name"] = proj_name
    #         result["quotation_name"] = quotation_name
    #         result["quotation_ver"] = quotation_ver
    #         result["feature_list"] = func_list
    #         result["columns"] = obj_quotation.get_func_columns()
    #         result["column_num"] = obj_quotation.get_func_column_num()
    #         # from app.ctrl.ctrl_user_group import CtrlUserGroup
    #         # result["group_list"] = CtrlUserGroup().get_groups_and_sub_by_proj(2, q_obj.proj_id)  # 2 SGL角色
    #         return True, result
    #     else:
    #         return False, "无数据"

    def get_feature_list2(self, quotation_id, user_id):
        q_obj = self.get_quotation_by_id(quotation_id)
        result = {"feature_list": [], "columns": [], "column_num": 0}
        if q_obj:
            quotation_name = q_obj.quotation_name
            quotation_ver = q_obj.quotation_ver
            proj_obj = q_obj.projects
            proj_name = proj_obj.insideName.inside_name
            proj_id = proj_obj.proj_id
            my_groups = CtrlUserGroup().get_my_group(user_id, proj_id)
            my_group_ids = [group.get("group_id") for group in my_groups]
            obj_quotation = get_ds_quotation(quotation_id)
            func_df = obj_quotation.get_diff_color_func(my_group_ids)
            func_group_df = obj_quotation.get_func_group_df2()
            merged_func_df = obj_quotation.merge_func_group_name(func_df, func_group_df)
            sgl_groups = CtrlUserGroup().get_project_sgl_group(proj_id)
            sgl_group_names = [group.get("group_name") for group in sgl_groups]
            df_columns = merged_func_df.columns.tolist()
            for sgl_group in sgl_group_names:
                if sgl_group not in merged_func_df.columns:
                    merged_func_df[sgl_group] = None
                else:
                    df_columns.remove(sgl_group)
            new_columns = df_columns+sgl_group_names
            merged_func_df = merged_func_df[new_columns]
            func_list = merged_func_df.to_dict(orient="records")
            # result["my_group"] = my_group.get("group_name")
            result["proj_id"] = proj_id
            result["proj_name"] = proj_name
            result["quotation_name"] = quotation_name
            result["quotation_ver"] = quotation_ver
            result["feature_list"] = func_list
            result["columns"] = obj_quotation.get_func_columns() + sgl_group_names
            result["group_list"] = sgl_group_names
            # result["column_num"] = obj_quotation.get_func_column_num()
            # from app.ctrl.ctrl_user_group import CtrlUserGroup
            # result["group_list"] = CtrlUserGroup().get_groups_and_sub_by_proj(2, q_obj.proj_id)  # 2 SGL角色
            return True, result
        else:
            return False, "无数据"

    # def load_func_cats(self, func_df, merged_func_df):
    #     cat_ids = [int(n) for n in list(func_df[Functions.category_id.name].unique())]
    #     q = (db.session.query(Category)
    #          .filter(Category.category_id.in_(cat_ids))
    #          .order_by(Category.category_id)
    #          )
    #     cat_df = pd.read_sql(q.statement, db.session.bind, index_col=Category.category_id.name)
    #     new_df = pd.merge(merged_func_df, cat_df, left_on=Functions.category_id.name,
    #                       right_index=True, how='left')
    #     new_list = new_df.to_dict(orient='records')
    #     new_list = self.find_children_group(new_list)
    #     return new_list

    def find_children_group(self, new_list, proj_id):
        group_df = get_group_df()
        gl_sgl_df = get_gl_sgl_df(proj_id)
        for item in new_list:
            if item['group_id']:
                group_id = item['group_id']
                group_name = group_df[group_df["group_id"] == group_id]["group_name"].tolist()[0]
                sgl_df = gl_sgl_df[gl_sgl_df["group_id"] == group_id]
                if not sgl_df.empty:
                    sgl_group_name = sgl_df["parent_group_name"].tolist()[0]
                    # 当大组存在时， 组信息要带上大组
                    item["group_id"] = [sgl_group_name, group_name]
                else:
                    item["group_id"] = [group_name]
            else:
                item['group_id'] = []
        return new_list

    def feature_assign2(self, data, quotation_id):
        try:
            if data:
                for func in data.get("feature_list"):
                    group_list = func.get("group_id")    # group_id 是个数组
                    func_id = func.get("func_id")
                    proj_id = db.session.query(Quotations).filter(Quotations.quotation_id == quotation_id).first().proj_id
                    if group_list:
                        success, msg = self.find_func_id_in_funcgroup_table(proj_id, group_list[-1], func_id)
                        if not success:
                            return False, msg
                        else:
                            group_id = msg
                            self.task_group_by_feature(func_id, group_id)
                    else:
                        q = (db.session.query(FuncGroup)
                             .filter(FuncGroup.func_id == func_id)
                             .all())
                        if q:
                            q[0].group_id = None
                            self.task_group_by_feature(func_id, group_id=None)
                    # TODO 这里可能添加履历
                db.session.commit()
                refresh_ds_quotation(quotation_id)
                return True, ''
            else:
                return False, "请不要传空数据"
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, str(e)

    def feature_assign_group(self, data_dict, quotation_id):
        try:
            group_df = get_group_df()
            # quotation_id = data_dict.get("quotation_id")
            proj_id = data_dict.get("proj_id")
            feature_list = data_dict.get("feature_list")
            sgl_groups = CtrlUserGroup().get_project_sgl_group(proj_id)
            sgl_group_names = [group.get("group_name") for group in sgl_groups]
            change_flag = False
            for feature in feature_list:
                func_id = feature.get("func_id")
                if feature.get("change"):
                    change_flag = True
                for group_name in sgl_group_names:
                    group_role = feature.get(group_name)
                    group_id = group_df.loc[group_df.group_name == group_name, Group.group_id.name].values[0]
                    group_id = int(group_id)
                    q = (db.session.query(FuncGroup)
                         .filter(FuncGroup.func_id == func_id)
                         .filter(FuncGroup.group_id == group_id)
                         .first())
                    if q:
                        if not group_role:
                            db.session.delete(q)
                            if q.group_role == "major":
                                self.task_group_by_feature(func_id, group_id=None)
                        else:
                            q.group_role = group_role
                            if group_role == "major":
                                self.task_group_by_feature(func_id, group_id)
                    else:
                        if group_role:
                            self.add_funcgroup_into_table(group_id, func_id, group_role)
                            if group_role == "major":
                                self.task_group_by_feature(func_id, group_id)
            db.session.commit()
            if change_flag:
                refresh_ds_quotation(quotation_id)
            return True, ''
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, str(e)

    def task_group_by_feature(self, func_id, group_id):
        """默认task的group要继承feature的分配的担当组"""
        q_list = db.session.query(Task).filter(Task.func_id == func_id).all()
        if len(q_list) == 1:
            default_task = q_list[0]
            if not (default_task.task1 or default_task.task2 or
                    default_task.task3 or default_task.task4 or
                    default_task.task5 or default_task.task6):
                default_task.group_id = group_id

    def feature_history(self, quotation_id):
        try:
            refresh_ds_quotation(quotation_id)
            obj_quotation = get_ds_quotation(quotation_id)
            fun_task_manday_df = obj_quotation.get_func_task_manday()
            manday_df = obj_quotation.get_manday_df()
            lastest_total_manday = manday_df[FuncManDay.days.name].sum()
            feature_history = []
            for index, row in fun_task_manday_df.iterrows():
                fh_d = dict()
                version = row[FuncManDay.version.name]
                if 1 == version:
                    continue
                fh_d["manday"] = lastest_total_manday
                fh_d["update_comment"] = row[FuncManDay.comment.name]
                cur_manday = row[FuncManDay.days.name]
                pre_manday = np.nan_to_num(fun_task_manday_df[
                                               (fun_task_manday_df[FuncManDay.group_id.name] == row[
                                                   FuncManDay.group_id.name])
                                               & (fun_task_manday_df[FuncManDay.option_id.name] == row[
                                                   FuncManDay.option_id.name])
                                               & (fun_task_manday_df[FuncManDay.task_id.name] == row[
                                                   FuncManDay.task_id.name])
                                               & (fun_task_manday_df[FuncManDay.version.name] == version - 1)][
                                               FuncManDay.days.name].values[0])
                lastest_total_manday = lastest_total_manday - cur_manday + pre_manday
                feature_history.append(fh_d)
            feature_history.append(dict(manday=lastest_total_manday, update_comment="initial"))
            # print(feature_history)
            return True, feature_history
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, str(e)

    def find_func_id_in_funcgroup_table(self, proj_id, group_name, func_id):
        # if group_id == '':
        #     group_id = None
        q = (db.session.query(FuncGroup)
             .filter(FuncGroup.func_id == func_id)
             .all())
        group = (db.session.query(Group)
                 .outerjoin(UserRole, Group.group_id == UserRole.group_id)
                 .filter(UserRole.proj_id == proj_id)
                 .filter(Group.group_name.ilike(group_name))
                 .first())
        if not group:
            return False, '有未在体制表中的组，请在体制表中添加此组：' + group_name
        if q:
            q[0].group_id = group.group_id
        else:
            self.add_funcgroup_into_table(group.group_id, func_id)
        return True, group.group_id

    def add_funcgroup_into_table(self, group_id, func_id, group_role="major"):
        funcgroup_info = {
            FuncGroup.group_id.name: group_id,
            FuncGroup.func_id.name: func_id,
            FuncGroup.group_role.name: group_role
        }
        funcgroup = FuncGroup(**funcgroup_info)
        db.session.add(funcgroup)

    def get_option_by_quotation_id(self, quotation_id):
        q = (db.session.query(Options)
             .filter(Options.quotation_id == quotation_id)
             .order_by(Options.option_id).all())
        options = []
        if q:
            for i_option in q:
                option = dict()
                option["option_name"] = i_option.option_name
                option["option_id"] = i_option.option_id
                option["quotation_id"] = i_option.quotation_id
                option["option_value_list"] = []
                for op_value in i_option.option_value:
                    option["option_value_list"].append({
                        "value_id": op_value.value_id,
                        "option_id": op_value.option_id,
                        "option_value": op_value.option_value,
                    })
                options.append(option)
        return options

    def get_option_by_quotation_id3(self, quotation_id):
        q = (db.session.query(Options)
             .filter(Options.quotation_id == quotation_id)
             .order_by(Options.option_id).all())
        options = []
        if q:
            for i_option in q:
                option = dict()
                option["option_name"] = i_option.option_name
                option["option_id"] = i_option.option_id
                option["quotation_id"] = i_option.quotation_id
                options.append(option)
        return options

    def get_option_list(self, quotation_id):
        q = (db.session.query(Options)
             .filter(Options.quotation_id == quotation_id)
             .order_by(Options.option_id).all())
        options = []
        if q:
            for i_option in q:
                option = dict()
                option["option_name"] = i_option.option_name
                option["option_id"] = i_option.option_id
                option["quotation_id"] = i_option.quotation_id
                options.append(option)
        return options

    def add_option_by_quotation_id(self, quotation_id, data):
        try:
            if data:
                quo = db.session.query(Quotations).filter(Quotations.quotation_id == quotation_id).all()
                op_id = self.add_option(quo.proj_id, quotation_id, data)
                for op_value in data.get("option_value_list"):

                    self.add_option_value_to_table(op_id, op_value)
            db.session.commit()
            return True, ''
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, str(e)

    def add_option_by_quotation_id3(self, quotation_id, data):
        try:
            if data:
                quo = db.session.query(Quotations).filter(Quotations.quotation_id == quotation_id).all()
                if not quo:
                    return False, "没有此报价，无法添加Option，请刷新页面"
                op_id = self.add_option(quo.proj_id, quotation_id, data)

            db.session.commit()
            return True, op_id
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, str(e)

    def add_option_by_quotation_id2(self, quotation_id, data):
        try:
            if data:
                quo = db.session.query(Quotations).filter(Quotations.quotation_id == quotation_id).all()
                if not quo:
                    return False, "没有此报价，无法添加Option，请刷新页面"
                if data.get("option_id") == 0 or (not data.get("option_id")):
                    op_id = self.add_option(quo[0].proj_id, quotation_id, data)
                    for op_value in data.get("option_value_list"):
                        self.add_option_value_to_table(op_id, op_value)
                else:
                    op_id = data.get("option_id")
                    option_value_list = self.get_option_value_list(op_id)
                    new_list = []
                    for op_value in data.get("option_value_list"):
                        if op_value.get("value_id") and op_value.get("value_id") != 0:
                            new_list.append(op_value.get("value_id"))
                        elif op_value.get("value_id") == 0:
                            self.add_option_value_to_table(op_id, op_value)
                    comb_id_list = self.old_combination_id_list(quotation_id)
                    for old_value in option_value_list:
                        if old_value not in new_list:
                            # 删掉old_value
                            success = self.del_option_value(old_value, comb_id_list)
                            if not success:
                                return False, "此option_value被使用,无法被删除"
                db.session.commit()
            return True, ''
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, str(e)

    def old_combination_id_list(self, quotation_id):
        q = (db.session.query(OptionCombination)
             .filter(OptionCombination.quotation_id == quotation_id)
             .all())
        comb_id_list = []
        for i_comb in q:
            if i_comb.option_value_id_list:
                id_list = i_comb.option_value_id_list.split(',')
                comb_id_list = list(set(id_list + comb_id_list))
        return comb_id_list

    def del_option_value(self, option_value_id, comb_id_list):
        if option_value_id in comb_id_list:
            return False
        db.session.query(OptionValue).filter(OptionValue.value_id == option_value_id).delete()
        return True

    def show_one_quotation_status(self, quotation_id):
        q = db.session.query(Quotations).filter(Quotations.quotation_id == quotation_id).first()
        if q:
            statue = q.status
            return True, statue
        else:
            return False, "已被删除或没有此条报价信息"

    def update_quotation_status(self, info):
        q = (db.session.query(Quotations)
             .filter(Quotations.quotation_id == info.get("quotation_id"))
             .first())
        if q:
            if q.status == "1":
                q.status = "2"
                db.session.commit()
                return True, ""
            else:
                return False, "此报价已为进行中无需变更状态"
        else:
            return False, "指定的报价不存在! quotation_id=%s" % info.get("quotation_id")

    def get_option_value_list(self, option_id):
        q = (db.session.query(OptionValue)
             .filter(OptionValue.option_id == option_id)
             .all())
        value_list = []
        for value in q:
            value_list.append(value.value_id)
        return value_list

    def get_combination_by_quotation_id(self, quotation_id):
        q = (db.session.query(OptionCombination)
             .filter(OptionCombination.quotation_id == quotation_id)
             .order_by(OptionCombination.id).all())
        combinations = []
        if q:
            for i_combination in q:
                combination = dict()
                combination["id"] = i_combination.id
                combination["option_value_id_list"] = i_combination.option_value_id_list
                combination["quotation_id"] = i_combination.quotation_id
                combination["value"] = i_combination.value
                combinations.append(combination)
        return True, combinations

    def get_combination_by_quotation_id3(self, quotation_id):
        q = (db.session.query(OptionCombination)
             .filter(OptionCombination.quotation_id == quotation_id)
             .order_by(OptionCombination.id).all())
        combinations = []
        if q:
            for i_combination in q:
                combination = dict()
                if i_combination.value == "Default":
                    combination["disable_delete"] = True
                else:
                    combination["disable_delete"] = self.find_combination_in_FuncManDay(i_combination.id)
                combination["id"] = i_combination.id
                combination["quotation_id"] = i_combination.quotation_id
                combination["proj_id"] = i_combination.proj_id
                combination["value"] = i_combination.value
                combination["checked"] = i_combination.checked
                combinations.append(combination)
        return True, combinations

    def add_combination_by_quotation_id(self, quotation_id, data):
        try:
            if data:
                comb_id_list = self.get_combination_id_list(quotation_id)
                new_list = []
                for i_combination in data:
                    if (i_combination.get("id") == 0) or (i_combination.get("id") == 'undefined'):
                        self.add_combination_to_table(quotation_id, i_combination)
                    else:
                        new_list.append(i_combination.get("id"))
                        self.update_combination_to_table(i_combination)
                # TODO 暂时禁用删除
                # for old_id in comb_id_list:
                #     if old_id not in new_list:
                #         self.del_combination(old_id)
            db.session.commit()
            return True, ''
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, str(e)

    def add_combination_by_quotation_id3(self, quotation_id, data):
        try:
            if data:
                for i_combination in data:
                    if (i_combination.get("id") == 0) or (i_combination.get("id") == 'undefined'):
                        self.add_combination_to_table3(quotation_id, i_combination)
                    else:
                        self.update_combination_to_table3(i_combination)
            db.session.commit()
            return True, ''
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, str(e)

    def find_combination_in_FuncManDay(self, comb_id):
        q = db.session.query(FuncManDay).filter(FuncManDay.option_id == comb_id).all()
        if q:
            return True
        else:
            return False

    def del_combination(self, comb_id):
        flag = self.find_combination_in_FuncManDay(comb_id)
        if not flag:
            db.session.query(OptionCombination).filter(OptionCombination.id == comb_id).delete()
            db.session.commit()
            return True, "OK"
        else:
            return False, "不能被删除"

    def get_combination_id_list(self, quotation_id):
        q = (db.session.query(OptionCombination)
             .filter(OptionCombination.quotation_id == quotation_id)
             .order_by(OptionCombination.id).all())
        combinations = []
        if q:
            for i_combination in q:
                combinations.append(i_combination.id)
        return combinations

    def get_checked_combination_id(self, quotation_id):
        q = (db.session.query(OptionCombination)
             .filter(OptionCombination.quotation_id == quotation_id)
             .filter(OptionCombination.checked == True)
             .order_by(OptionCombination.id).all())
        combinations = []
        if q:
            for i_combination in q:
                combinations.append(i_combination.id)
        return combinations

    def update_combination_to_table(self, data):
        q = (db.session.query(OptionCombination)
             .filter(OptionCombination.id == data.get("id"))
             .first())
        if q:
            q.option_value_id_list = data.get("option_value_id_list")
            q.value = data.get("value")

    def update_combination_to_table3(self, data):
        q = (db.session.query(OptionCombination)
             .filter(OptionCombination.id == data.get("id"))
             .first())
        if q:
            q.checked = data.get("checked")

    def add_combination_to_table(self, quotation_id, data):
        combination_info = {
            OptionCombination.quotation_id.name: quotation_id,
            OptionCombination.option_value_id_list.name: data.get("option_value_id_list"),
            OptionCombination.value.name: data.get("value"),
        }
        combination = OptionCombination(**combination_info)
        db.session.add(combination)

    def add_combination_to_table3(self, quotation_id, data):
        combination_info = {
            OptionCombination.quotation_id.name: quotation_id,
            OptionCombination.checked.name: data.get("checked"),
            OptionCombination.value.name: data.get("value"),
        }
        combination = OptionCombination(**combination_info)
        db.session.add(combination)

    def add_option_value_to_table(self, option_id, info):
        value_info = {
            OptionValue.option_value.name: info.get("option_value"),
            OptionValue.option_id.name: option_id,
        }
        value_info = OptionValue(**value_info)
        db.session.add(value_info)

    # def add_option_by_quotation_id(self, quotation_id, data):
    #     try:
    #         for i_option in data:
    #             q = (db.session.query(Options)
    #                  .filter(Options.quotation_id == quotation_id)
    #                  .filter(Options.option_id == i_option.option_id)
    #                  .order_by(Options.option_id).all())
    #             if q:
    #                 q[0].option_name = data.get("option_name")
    #                 q[0].update_time = self.get_current_time()
    #             else:
    #                 quo = db.session.query(Quotations).filter(Quotations.quotation_id == quotation_id).all()
    #                 self.add_option(quo.proj_id, quotation_id, i_option)
    #         db.session.commit()
    #         return True, ''
    #     except Exception as e:
    #         db.session.rollback()
    #         current_app.logger.error('%s' % str(e))
    #         return False, str(e)

    def add_option(self, proj_id, quo_id, data):
        """
        新增option
        :param proj_id:
        :param quo_id:
        :param data:
        :return:
        """
        option_info = {
            Options.option_name.name: data.get("option_name"),
            Options.create_time.name: self.get_current_time(),
            Options.update_time.name: self.get_current_time(),
            Options.proj_id.name: proj_id,
            Options.quotation_id.name: quo_id,
        }
        option_info = Options(**option_info)
        db.session.add(option_info)
        db.session.flush()
        return option_info.option_id

    def get_quotation_pie(self, quotation_id):
        try:
            result = dict()
            # group by feature[category]
            feature_list = []
            # refresh_ds_quotation(quotation_id)
            obj_quotation = get_ds_quotation(quotation_id)
            sum_manday_by_category = obj_quotation.summary_manday_by_category()
            sum_manday_by_category = sum_manday_by_category.reset_index(Category.category_name.name)
            for index, row in sum_manday_by_category.iterrows():
                feature_d = dict()
                feature_d["name"] = row[Category.category_name.name]
                feature_d["value"] = row[FuncManDay.days.name]
                feature_list.append(feature_d)
            result["Feature"] = feature_list

            # # group by GL
            gl_list = []
            sum_manday_by_gl = obj_quotation.summary_manday_by_gl()
            sum_manday_by_gl = sum_manday_by_gl.reset_index(Group.group_name.name)
            for index, row in sum_manday_by_gl.iterrows():
                gl_d = dict()
                gl_d["name"] = row[Group.group_name.name]
                gl_d["value"] = row[FuncManDay.days.name]
                gl_list.append(gl_d)
            result["GL"] = gl_list

            # # group by SGL
            # # task must be assigned to gl, its parent group owner must be sgl
            sgl_list = []
            sum_manday_by_sgl = obj_quotation.summary_manday_by_sgl()
            sum_manday_by_sgl = sum_manday_by_sgl.reset_index(Users.user_name.name)
            for index, row in sum_manday_by_sgl.iterrows():
                sgl_d = dict()
                sgl_d["name"] = row[Users.user_name.name]
                sgl_d["value"] = row[FuncManDay.days.name]
                sgl_list.append(sgl_d)
            result["SGL"] = sgl_list

            # print(result)

            result_text = json.dumps(result)

            return True, result_text
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, str(e)

    def get_group_list(self, user_id, quotation_id):
        """根据报价取组和子组"""
        group_list = []
        group_ids = []  # 只包含子组的id
        parent_sub_group_ids = []  # 包含父子组的所有id
        quotation_obj = self.get_quotation_by_id(quotation_id)
        proj_id = quotation_obj.proj_id
        q_groups = (db.session.query(Group)
                    .outerjoin(UserRole, Group.group_id == UserRole.group_id)
                    .filter(UserRole.proj_id == proj_id)
                    .filter(UserRole.user_id == user_id)
                    .order_by(Group.group_name))
        q_obj_list = []  # 只存没有子组的组
        parent_sub_q_list = []  # 有父组又有子组
        for group in q_groups:
            self.get_sub_group(group, q_obj_list, proj_id, parent_sub_q_list)
        for q_obj in q_obj_list:
            group_ids.append(q_obj.group_id)
            group_list.append({"group_id": q_obj.group_id, "group_name": q_obj.group_name})
        for q in parent_sub_q_list:
            parent_sub_group_ids.append(q.group_id)
        return group_list, group_ids, parent_sub_group_ids

    def get_my_and_sub_group_owner_users(self, user_id, proj_id=None):
        """
        取我的组和子组的group_id
        :param user_id:
        :return:
        """
        ctrl_group = CtrlUserGroup()
        my_groups = ctrl_group.get_my_group(user_id, proj_id)
        my_group_ids = [group.get("group_id") for group in my_groups]
        my_sub_group = ctrl_group.get_sub_groups(my_group_ids)
        group_id_list = [group.get("group_id") for group in my_sub_group] + my_group_ids
        return group_id_list

    def get_group_list_by_df(self, group_id_list, proj_id, parent_group_id_list):
        """根据报价取组和子组"""
        group_list = []
        group_ids = []  # 只包含子组的id
        parent_sub_group_ids = []  # 包含父子组的所有id
        q_groups = (db.session.query(Group)
                    .outerjoin(UserRole, Group.group_id == UserRole.group_id)
                    .filter(UserRole.proj_id == proj_id)
                    .filter(UserRole.group_id.in_(group_id_list))
                    .order_by(Group.group_name))
        # q_obj_list = []  # 只存没有子组的组
        # parent_sub_q_list = []  # 有父组又有子组
        for group in q_groups:
            if group.group_id not in set(parent_group_id_list):
                group_ids.append(group.group_id)
                group_list.append({"group_id": group.group_id, "group_name": group.group_name})
            parent_sub_group_ids.append(group.group_id)
        return group_list, group_ids, parent_sub_group_ids

    def get_sub_group(self, parent_q, sub_list, proj_id, parent_sub_list):
        sub_groups = (db.session.query(Group)
                      .outerjoin(UserRole, Group.group_id == UserRole.group_id)
                      .filter(UserRole.proj_id == proj_id)
                      .filter(Group.parent_group_id == parent_q.group_id)
                      .order_by(Group.group_name)
                      .all())
        if sub_groups:
            parent_sub_list.append(parent_q)
            for sub in sub_groups:
                self.get_sub_group(sub, sub_list, proj_id, parent_sub_list)
        else:
            parent_sub_list.append(parent_q)
            sub_list.append(parent_q)

    def not_assign_function_sgl(self, parent_group_ids, group_ids, quotation_id):
        """
        统计SGl的未分配的function的件数
        未分配：只分配给了大组，没有分配给小组的
        :param my_group_id: SGL组的group_id
        :param my_group_id: 报价id
        :return:
        """
        if group_ids:
            q = (db.session.query(Functions.func_id)
                 .outerjoin(FuncGroup, Functions.func_id == FuncGroup.func_id)
                 .filter(Functions.quotation_id == quotation_id)
                 .filter(FuncGroup.group_id.in_(parent_group_ids)))
            count_not_assign = q.count()  # 未分配的
        else:
            count_not_assign = 0  # 没有子组时就不需要分配
        return count_not_assign

    def not_assign_function_sales(self, quotation_id):
        """
            统计SALES的未分配的function的件数
            未分配：没有分配组的function
            :param quotation_id: 报价id
            :return:
        """
        q1 = (db.session.query(Functions.func_id, FuncGroup.group_id)
              .outerjoin(FuncGroup, Functions.func_id == FuncGroup.func_id)
              .filter(Functions.quotation_id == quotation_id)
              .filter(FuncGroup.group_id.is_(None)))
        count_not_assign = q1.count()  # 未分配的
        return count_not_assign

    def not_confirm_task_sgl(self, group_id_list, quotation_id):
        """
        待确认： 工数没有被全部确认的task(SGL)
        :param group_id_list:
        :param quotation:
        :return:
        """
        task_id_q, my_task_q = self.get_my_task_query(group_id_list, quotation_id)
        task_ids = []
        if task_id_q:
            task_ids = [q[0] for q in task_id_q]
        mayday_q = (db.session.query(FuncManDay.task_id, FuncManDay.group_id,
                                     FuncManDay.option_id,
                                     func.max(FuncManDay.id))
                    .filter(FuncManDay.task_id.in_(task_ids))
                    .filter(FuncManDay.group_id.in_(group_id_list))
                    .group_by(FuncManDay.task_id, FuncManDay.group_id,
                              FuncManDay.option_id).all()
                    )  # 取关于我的task的所填的最新工数
        if not mayday_q:
            count_not_confirm = 0
        else:
            manday_ids = [q[3] for q in mayday_q]  # 取最新版本工数的id
            q = (db.session.query(Task.task_id)
                 .join(FuncManDay, Task.task_id == FuncManDay.task_id)
                 .filter(Task.task_id.in_(task_ids))
                 .filter(FuncManDay.id.in_(manday_ids))
                 .filter(or_(FuncManDay.days.isnot(None),
                             FuncManDay.pre_id.isnot(None),
                             and_(FuncManDay.comment.isnot(None), FuncManDay.comment != ''),
                             FuncManDay.status_id.isnot(None)
                             )
                         )
                 .filter(or_(FuncManDay.status_id == 3,
                             FuncManDay.status_id.is_(None))).distinct()
                 )
            count_not_confirm = q.count()  # 待确认的
        return count_not_confirm

    def not_quotation_task_gl(self, group_id_list, quotation_id):
        """
        待报价：没有填写工数的task和状态是新建；处理中或者为空的task
        :param group_id_list:
        :param quotation_id:
        :return:
        """
        task_id_q, my_task_q = self.get_my_task_query(group_id_list, quotation_id)
        task_ids = []
        my_task_ids = []
        if task_id_q:
            task_ids = [q[0] for q in task_id_q]
        if my_task_q:
            my_task_ids = [q[0] for q in my_task_q]
        not_my_task = [task_id for task_id in task_ids if task_id not in my_task_ids]
        mayday_q = (db.session.query(FuncManDay.task_id, FuncManDay.group_id,
                                     FuncManDay.option_id,
                                     func.max(FuncManDay.id))
                    .filter(FuncManDay.task_id.in_(task_ids))
                    .filter(FuncManDay.group_id.in_(group_id_list))
                    .group_by(FuncManDay.task_id, FuncManDay.group_id,
                              FuncManDay.option_id).all()
                    )  # 取关于我的task的所填的最新工数
        if not mayday_q:
            count_not_quotation = len(task_ids)
        else:
            manday_task_ids = set([q[0] for q in mayday_q])  # 有填过工数的task_id
            manday_ids = [q[3] for q in mayday_q]  # 取最新版本工数的id
            count_no_cost = len(task_ids) - len(manday_task_ids)  # 没有填工数的task
            q3 = (db.session.query(Task.task_id)
                  .outerjoin(FuncManDay, Task.task_id == FuncManDay.task_id)
                  .filter(and_(FuncManDay.id.in_(manday_ids),
                               or_(Task.task_id.in_(my_task_ids),
                                   and_(Task.task_id.in_(not_my_task),
                                        or_(FuncManDay.days.isnot(None),
                                            FuncManDay.pre_id.isnot(None),
                                            and_(FuncManDay.comment.isnot(None), FuncManDay.comment != ''),
                                            FuncManDay.status_id.isnot(None)
                                            )
                                        )
                                   )
                               )
                          )
                  .filter(or_(FuncManDay.status_id.in_([1, 2]),  # 报价状态是新建，处理中
                              FuncManDay.status_id.is_(None),
                              FuncManDay.id.is_(None))).distinct()
                  )  # 工数信息都为空和工数状态是新建；处理中或者为空的task(gl)
            count_not_quotation = q3.count() + count_no_cost  # 待待报价的
        return count_not_quotation

    def issue_task(self, group_id_list, quotation_id):
        """
        指摘：有工数被指摘的task
        :param group_id_list:
        :param quotation_id:
        :return:
        """
        task_id_q, my_task_q = self.get_my_task_query(group_id_list, quotation_id)
        task_ids = []
        if task_id_q:
            task_ids = [q[0] for q in task_id_q]
        mayday_q = (db.session.query(FuncManDay.task_id, FuncManDay.group_id,
                                     FuncManDay.option_id,
                                     func.max(FuncManDay.id))
                    .filter(FuncManDay.task_id.in_(task_ids))
                    .group_by(FuncManDay.task_id, FuncManDay.group_id,
                              FuncManDay.option_id))  # 取关于我的task的所填的最新工数
        if group_id_list:
            mayday_q = mayday_q.filter(FuncManDay.group_id.in_(group_id_list)).all()
        else:
            mayday_q = mayday_q.all()
        if not mayday_q:
            count_issue = 0
        else:
            manday_ids = [q[3] for q in mayday_q]
            issue_q = (db.session.query(Issue.key_id,
                                     func.max(Issue.issue_id))
                       .filter(Issue.table_name == "func_man_day")
                       .group_by(Issue.key_id
                              ))  # 取每条工数的最新指摘
            issue_ids = [q[1] for q in issue_q]
            q = (db.session.query(Task.task_id)
                 .outerjoin(FuncManDay, Task.task_id == FuncManDay.task_id)
                 .outerjoin(Issue, FuncManDay.base_id == Issue.key_id)
                 .filter(FuncManDay.id.in_(manday_ids))
                 .filter(Issue.issue_id.in_(issue_ids))
                 .filter(Issue.status.in_(["打开"])).distinct())
            # issue状态：["打开", "已确认", "关闭"]
            count_issue = q.count()  # 有指摘的
        return count_issue

    def get_my_task_query(self, group_id_list, quotation_id):
        """"
        我的task:分配到我的的task
        1, 分配到我的的task（function分配的和task分配的）
        2，没分配到我的但我填填过的task
        """
        q1 = (db.session.query(Task.task_id)
              .outerjoin(Functions, Task.func_id == Functions.func_id)
              .outerjoin(FuncGroup, Functions.func_id == FuncGroup.func_id)
              .filter(Functions.quotation_id == quotation_id)
              .filter(Task.delete.is_(False))
              )  # 查询分配到我的的task
        q2 = (db.session.query(FuncManDay.task_id)
              .outerjoin(Task, FuncManDay.task_id == Task.task_id)
              .outerjoin(Functions, Task.func_id == Functions.func_id)
              .filter(Functions.quotation_id == quotation_id)
              .filter(Task.delete.is_(False))
              )  # 查询我填过的task

        if group_id_list:
            q1 = q1.filter(or_(Task.group_id.in_(group_id_list), FuncGroup.group_id.in_(group_id_list)))
            q2 = q2.filter(FuncManDay.group_id.in_(group_id_list))
        task_id_q = q1.union(q2)
        task_id_q = task_id_q.distinct().all()
        return task_id_q, q1.all()

    # def delete_quotation(self, quotation_id):
    #     """删除报价"""
    #     del_man_day = (db.session.query(FuncManDay)
    #                    .outerjoin(Task, FuncManDay.task_id == Task.task_id)
    #                    .outerjoin(Functions, Task.func_id == Functions.func_id)
    #                    .filter(Functions.quotation_id == quotation_id))



