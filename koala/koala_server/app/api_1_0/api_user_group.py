
from token_manage import auth
from flask_restful import Resource, request
from app.ctrl.ctrl_user import CtrlUser
from app.ctrl.ctrl_user_group import CtrlUserGroup


class ApiAllUser(Resource):
    @auth.login_required
    def get(self):
        result = {"result": "OK", "content": []}
        user_list = CtrlUser().get_all_user()
        if user_list:
            result["result"] = "OK"
            result["content"] = user_list
        return result


class ApiAllGroup(Resource):
    @auth.login_required
    def get(self):
        result = {"result": "OK", "content": []}
        user_list = CtrlUserGroup().get_all_groups()
        if user_list:
            result["result"] = "OK"
            result["content"] = user_list
        return result


class ApiManagerGroup(Resource):
    """项目体制组的删除与更新"""

    @auth.login_required
    def post(self):
        """更新"""
        result = {"result": "NG", "error": ""}
        data_json = request.get_json(force=True)
        flag, msg = CtrlUserGroup().update_manager_group(data_json)
        if flag:
            result["result"] = "OK"
            result["content"] = msg
        else:
            result["error"] = msg
        return result

    @auth.login_required
    def delete(self, proj_id, group_id, commit_user):
        """删除"""
        result = {"result": "NG", "error": ""}
        flag, error = CtrlUserGroup().delete_manager_group(proj_id, group_id, commit_user)
        if flag:
            result["result"] = "OK"
        else:
            result["error"] = error
        return result


class ApiManagerMemeber(Resource):
    """项目体制增加组员"""

    @auth.login_required
    def post(self):
        """更新"""
        result = {"result": "NG", "error": ""}
        data_json = request.get_json(force=True)
        flag, error = CtrlUserGroup().update_manager_member(data_json)
        if flag:
            result["result"] = "OK"
        else:
            result["error"] = error
        return result

    @auth.login_required
    def delete(self, proj_id, group_id, user_id, commit_user):
        """删除"""
        result = {"result": "NG", "error": ""}
        flag, error = CtrlUserGroup().delete_manager_member(proj_id, group_id, user_id, commit_user)
        if flag:
            result["result"] = "OK"
        else:
            result["error"] = error
        return result


class ApiProjectGroups(Resource):
    @auth.login_required
    def get(self, proj_id):
        result = {"result": "OK", "content": []}
        group_list = CtrlUserGroup().get_project_groups_tree(proj_id)
        if group_list:
            result["result"] = "OK"
            result["content"] = group_list
        return result


class ApiGroupsToTask(Resource):
    @auth.login_required
    def get(self, proj_id):
        result = {"result": "OK", "content": []}
        group_list = CtrlUserGroup().get_project_groups(proj_id)
        if group_list:
            result["result"] = "OK"
            result["content"] = group_list
        return result


