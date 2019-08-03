# -*- coding: UTF-8 -*-
import os
from app.ctrl.ctrl_project import CtrlProject
from flask_restful import Resource, request
from token_manage import auth


class ApiProjectState(Resource):
    @auth.login_required
    def get(self):
        result = {"result": "OK", "content": []}
        res = CtrlProject().get_proj_state_options()
        if res:
            result["result"] = "OK"
            result["content"] = res
        return result


class ApiProjectInside(Resource):
    @auth.login_required
    def get(self):
        result = {"result": "OK", "content": []}
        res = CtrlProject().get_inside_name_list()
        if res:
            result["result"] = "OK"
            result["content"] = res
        return result


class ApiProjectType(Resource):
    @auth.login_required
    def get(self):
        result = {"result": "OK", "content": []}
        res = CtrlProject().get_proj_type_list()
        if res:
            result["result"] = "OK"
            result["content"] = res
        return result


class ApiProjectNameCheck(Resource):
    @auth.login_required
    def get(self):
        result = {"result": "OK", "content": []}
        res = CtrlProject().check_proj_name()
        if res:
            result["result"] = "OK"
            result["content"] = res
        return result


class ApiProjectList(Resource):
    @auth.login_required
    def get(self, user_id=None):
        result = {"result": "OK", "content": []}
        if user_id:
            res = CtrlProject().get_proj_list_by_user_id(user_id)
        else:
            res = CtrlProject().get_proj_list()
        if res:
            result["result"] = "OK"
            result["content"] = res
        return result

    @auth.login_required
    def post(self):
        result = {"result": "NG"}
        data = request.get_json(force=True)
        if data:
            proj_id, message = CtrlProject().add_project_with_observer(data)
            if proj_id:
                result = {"result": "OK", 'content': proj_id}
            else:
                result["error"] = message
        else:
            result["error"] = "请不要传空数据"
        return result


class ApiProjectInfo(Resource):
    @auth.login_required
    def get(self, pro_id):
        result = {"result": "NG", "content": []}
        res, msg = CtrlProject().get_one_proj_by_id(pro_id)
        if res:
            result["result"] = "OK"
            result["content"] = msg
        else:
            result["content"] = msg
        return result

    @auth.login_required
    def put(self, pro_id):
        result = {"result": "NG"}
        data = request.get_json(force=True)
        if data:
            proj_id, message = CtrlProject().change_proj_by_id_with_observer(pro_id, data)
            if proj_id:
                result = {"result": "OK", 'content': proj_id}
            else:
                result["error"] = message
        else:
            result["error"] = "请不要传空数据"
        return result

    # @auth.login_required
    def post(self):
        result = {"result": "NG"}
        data = request.get_json(force=True)
        # data = request
        if data:
            proj_id, message = CtrlProject().delete_proj_by_id(data)
            if proj_id:
                result = {"result": "OK", 'content': proj_id}
            else:
                result["error"] = message
        else:
            result["error"] = "请不要传空数据"
        return result


class ApiProjectManager(Resource):
    """项目体制"""

    @auth.login_required
    def get(self, proj_id, user_id):
        result = {"result": "NG", "content": []}
        res, msg = CtrlProject().get_project_manager(proj_id, user_id)
        if res:
            result["result"] = "OK"
            result["content"] = msg
        else:
            result["error"] = msg
        return result


class ApiManageList(Resource):
    """项目体制option"""

    @auth.login_required
    def get(self):
        result = {"result": "NG", "content": []}
        res, msg = CtrlProject().get_manager_list()
        if res:
            result["result"] = "OK"
            result["content"] = msg
        else:
            result["error"] = msg
        return result


class ApiManagerImport(Resource):
    """项目体制导入"""

    # def get(self):
    #     """测试"""
    #     proj_id = 2
    #     file_path = r'C:\workspace\koala\Spec2DB\koala\koala_server\template\开发体制_template_ver0.1.xlsx'
    #     res, msg = CtrlProject().import_project_manager(file_path, proj_id)
    #     print(res, msg)
    @auth.login_required
    def post(self):
        result = {"result": "NG"}
        request_data = request
        res, msg = CtrlProject().import_manager(request_data)
        if res:
            result["result"] = "OK"
            result["content"] = res
        else:
            result["error"] = msg
        return result


