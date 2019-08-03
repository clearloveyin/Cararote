from ..service import *
from app.db import db
from app.controller.ctrl_project import CtrlProject


class ServiceProject(object):
    def __init__(self):
        self.ctrl_object = CtrlProject()

    def get_all_project(self):
        """获取所有项目"""
        ctrl_project = self.ctrl_object
        result = {"type": SUCCESS, "content": None}
        try:
            project_list = ctrl_project.get_all_project()
            if not project_list:
                result["type"] = NOT_DATA
                message = "暂无项目！"
                result["message"] = message
            else:
                result["content"] = project_list
            return result
        except Exception as e:
            result = return_exception_message(e)
            return result

    def get_one_project(self, proj_id):
        """获取单个项目"""
        ctrl_project = self.ctrl_object
        result = {"type": SUCCESS, "content": None}
        try:
            project_dict = ctrl_project.get_one_project(proj_id)
            if not project_dict:
                result["type"] = PROMPT_ERROR
                message = "项目id为%s的项目不存在！" % str(proj_id)
                current_app.logger.info(message)
                result["message"] = message
            else:
                result["content"] = project_dict
            return result
        except Exception as e:
            result = return_exception_message(e)
            return result

    def add_project_members(self, proj_id, project_members):
        """添加项目人员和角色"""
        ctrl_project = self.ctrl_object
        for member in project_members:
            user_id = member.get("user_id")
            role_id = member.get("role_id")
            ctrl_project.add_project_role(proj_id, user_id, role_id)

    def add_project(self, request_data):
        """添加新项目"""
        ctrl_project = self.ctrl_object
        result = {"type": SUCCESS, "content": None}
        proj_name = request_data.get("proj_name")
        describe = request_data.get("describe")
        commit_user = request_data.get("commit_user")
        project_members = request_data.get("project_members")
        if not proj_name:
            result["type"] = PROMPT_ERROR
            message = "项目名称不能为空！"
            current_app.logger.info(message)
            result["message"] = message
            return result
        new_project_data = {"proj_name": proj_name, "describe": describe,
                            "create_user": commit_user, "update_user": commit_user}
        try:
            proj_id = ctrl_project.add_project(new_project_data)
            self.add_project_members(proj_id, project_members)
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            result = return_exception_message(e)
            return result

    def edit_project_members(self, proj_id, project_members):
        """修改项目人员和角色"""
        ctrl_project = self.ctrl_object
        for member in project_members:
            user_id = member.get("user_id")
            role_id = member.get("role_id")
            ctrl_project.edit_project_role(proj_id, user_id, role_id)

    def edit_project_data(self, request_data):
        ctrl_project = self.ctrl_object
        result = {"type": SUCCESS, "content": None}
        proj_id = request_data.get("proj_id")
        proj_name = request_data.get("proj_name")
        describe = request_data.get("describe")
        commit_user = request_data.get("commit_user")
        project_members = request_data.get("project_members")
        new_project_data = {"proj_id": proj_id, "proj_name": proj_name,
                            "describe": describe, "update_user": commit_user}
        try:
            res = ctrl_project.edit_project(new_project_data)
            if not res:
                result["type"] = PROMPT_ERROR
                message = "项目id为%s的项目不存在！" % str(proj_id)
                current_app.logger.info(message)
                result["message"] = message
                return result
            self.edit_project_members(proj_id, project_members)
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            result = return_exception_message(e)
            return result
