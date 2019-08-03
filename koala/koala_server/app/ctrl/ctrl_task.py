import re
import copy
from app.ctrl.ctrl_quotations import CtrlQuotations
from app.db.quotations import *
from app.db.users import UserRole, Group
from app.data_server.ds_quotation import get_ds_quotation
from app.data_server.ds_quotation import refresh_ds_quotation
from app.data_server.ds_quotation import refresh_lastest_man_day_id
from app.data_server.ds_pieces import get_gl_sgl_df
from flask import current_app


class CtrlTask(CtrlQuotations):
    def __init__(self):
        CtrlQuotations.__init__(self)
        self.key_col = Task.task_id
        self.db_object = Task
        self.col_list = [Task.task1.name, Task.task2.name, Task.task3.name,
                         Task.task4.name, Task.task5.name, Task.task6.name,
                         Task.group_id.name]
        self.task_col_list = []
        for column in Task.__table__.columns:
            self.task_col_list.append(column.name)

    def get_quotations_task(self, quotation_id, user_id=0):
        """根据报价取task信息"""
        q_obj = self.get_quotation_by_id(quotation_id)
        result = {"task_list": [], "columns": [], "column_num": 0}
        if q_obj:
            quotation_name = q_obj.quotation_name
            quotation_ver = q_obj.quotation_ver
            proj_obj = q_obj.projects
            proj_name = proj_obj.insideName.inside_name
            proj_id = proj_obj.proj_id
            obj_quotation = get_ds_quotation(quotation_id)
            func_task_df = obj_quotation.get_func_task_df()
            func_task_df = func_task_df.fillna('')
            task_list = func_task_df.to_dict(orient="records")
            task_list = self.find_children_group(task_list, proj_id)
            result["proj_id"] = proj_id
            result["proj_name"] = proj_name
            result["quotation_name"] = quotation_name
            result["quotation_ver"] = quotation_ver
            result["task_list"] = task_list
            result["columns"] = obj_quotation.get_func_columns()+obj_quotation.get_task_columns()
            result["column_num"] = obj_quotation.get_func_column_num()+obj_quotation.get_task_column_num()
            return result
        else:
            return False

    def update_task(self, data_json):
        """更新task信息"""
        commit_user = data_json.get('commit_user')
        task_list = data_json.get('task_list')
        delete_task_list = data_json.get("delete_list")
        quotation_id = data_json.get('quotation_id')
        proj_id = data_json.get('proj_id')
        update_time = self.get_current_time()
        try:
            res, msg = self.delete_task(delete_task_list)
            if not res:
                return False, msg
            commit_list = []
            last_task = dict()  # 上一个task信息，为了补全上级task信息
            last_func_id = 0  # 上一个func_id, 与上一条task的func_id相同时才继承上级task信息
            for task in task_list:
                func_id = task.get("func_id")
                action = task.get("action")
                if func_id != last_func_id:
                    last_task = dict()
                self.get_new_task(task, commit_user, update_time)
                self.completion_task(task, last_task)
                last_func_id = func_id
                last_task = copy.deepcopy(task)  # 复制该条task信息
                if action == "change":
                    group_list = task.get("group_id")  # group_id 是个数组
                    if group_list:
                        res, msg = self.check_group_in_manager(group_list[-1], proj_id)
                        if not res:
                            return False, msg
                        else:
                            task["group_id"] = msg
                    else:
                        task["group_id"] = None
                    res, msg = self.update_one_task(task, action)
                    if res:
                        log_dict = msg
                        if log_dict:
                            commit_list.append(log_dict)
                    else:
                        return False, msg
            self.commit_log(commit_list, commit_user, update_time)
            db.session.commit()
            refresh_lastest_man_day_id()
            refresh_ds_quotation(quotation_id)
            return True, ""
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % e)
            return False, "服务异常！请联系管理员！"

    def delete_task(self, delete_task_list):
        """
        删除task把delete字段设为True
        :return:
        """
        if delete_task_list:
            for task in delete_task_list:
                task_id = task.get("task_id")
                task_db = self.get_task_by_id(task_id)
                if not task_db:
                    return False, "task_id:%s不存在！" % task_id
                task_db.delete = True
        return True, ""

    def check_group_in_manager(self, group_name, proj_id):
        """
        判断分配的组是否存在体质表中
        :param group_name:
        :param proj_id:
        :return:
        """
        group = (db.session.query(Group)
                 .outerjoin(UserRole, Group.group_id == UserRole.group_id)
                 .filter(UserRole.proj_id == proj_id)
                 .filter(Group.group_name.ilike(group_name))
                 .filter(Group.group_id != 1)  # 排除掉默认的PL组
                 .first())
        if not group:
            return False, '有未在体制表中的组，请在体制表中添加此组：' + group_name
        else:
            return True, group.group_id

    def check_delete_task(self, quotation_id, commit_user, task_id):
        """
        该条task的删除条件：
        1，该条task分在我的组或子组下or没有被分配
        2，该条task没有其他组填写工数，或工数信息全部为空
        :param quotation_id:
                commit_user:
                task_id:
        :return:
        """
        quotation_obj = self.get_quotation_by_id(quotation_id)
        proj_id = quotation_obj.proj_id
        group_list_df = get_gl_sgl_df(proj_id)
        parent_group_id_list = group_list_df["parent_group_id"].tolist()
        group_id_list = self.get_my_and_sub_group_owner_users(commit_user)
        group_list, group_ids, parent_sub_group_ids = self.get_group_list_by_df(group_id_list, proj_id, parent_group_id_list)
        task_db = self.get_task_by_id(task_id)
        if not task_db:
            return False, "task_id:%s不存在！" % task_id
        group_id = task_db.group_id
        # join_task = self.join_task_name(task_db)
        if group_id is not None and group_id not in parent_sub_group_ids:
            return False, "该条task不在您的组下，不能删除！"
        other_group_cost = self.get_other_group_cost(task_id, group_ids)
        for cost in other_group_cost:
            if (cost["days"] or cost["precondition"]
                    or cost["status"] or cost["comment"]):
                return False, "该条task有其他组填有工数信息，不能删除"
        return True, ""

    def get_other_group_cost(self, task_id, my_group_ids):
        """获取其他组下工数信息"""
        cost_list = []
        q = (db.session.query(FuncManDay)
             .filter(FuncManDay.task_id == task_id)
             .filter(FuncManDay.group_id.notin_(my_group_ids)))
        for cost in q:
            cost_list.append(cost.to_dict())
        return cost_list

    def join_task_name(self, task):
        """连接task信息"""
        if type(task) != dict:
            task = task.to_dict()
        task_name_list = []
        for key in task:
            p = re.compile(r'^%s\d+' % "task")
            match = p.search(key)
            if match:  # task1~N
                if task[key]:
                    task_name_list.append(task.get(key))
        join_task = "/".join(task_name_list)
        return join_task

    def get_task_by_id(self, task_id):
        q = (db.session.query(Task).filter(Task.task_id == task_id).first())
        return q

    def get_new_task(self, task, commit_user, update_time):
        self.remove_other(task)
        if not task.get("task_id"):
            task[Task.create_user.name] = commit_user
        if task.get(Task.group_id.name) == "":
            task[Task.group_id.name] = None
        task[Task.update_user.name] = commit_user
        task[Task.update_time.name] = update_time

    def remove_other(self, task_dict):
        """去除非task的字段"""
        key_list = list(task_dict.keys())
        for key in key_list:
            if key not in self.task_col_list:
                task_dict.pop(key)
            else:
                val = task_dict.get(key)
                if val and isinstance(val, str):
                    val = val.strip()  # 去掉尾部空格
                if val == '':
                    task_dict[key] = None
                else:
                    task_dict[key] = val

    def completion_task(self, task, last_task):
        """补全task信息"""
        if not last_task:
            return
        for key in list(task.keys()):
            p = re.compile(r'^%s\d+' % "task")
            match = p.search(key)
            if match:  # task1~N
                if not task[key]:
                    task[key] = last_task.get(key)
                else:
                    break

    def update_one_task(self, task, action):
        """更新一条task"""
        ctrl_task = CtrlTask()
        task_id = task.get("task_id")
        if task_id:
            old_tasks = self.get_old_data(Task, Task.task_id, task_id)
            old_task = old_tasks[0]
            res, msg = self.diff_ver(task.get("task_version"), old_task.get("task_version"))
            if not res:
                return False, "Task有人更新，请重新刷新页面！"
            # if action == "delete":
            #     task = copy.deepcopy(old_task)
            #     task[Task.delete.name] = True
        else:
            old_task = None
        task["delete"] = False
        task["task_version"] = self.update_version(task.get("task_version"))
        log_dict = self.common_add(ctrl_task.db_object, task, old_task, ctrl_task.col_list, ctrl_task.key_col)
        return True, log_dict



