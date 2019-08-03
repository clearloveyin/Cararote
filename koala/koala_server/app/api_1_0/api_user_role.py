from token_manage import auth
from flask_restful import Resource, request
from app.ctrl.ctrl_user import CtrlUser


class ApiUserRole(Resource):
    @auth.login_required
    def get(self):
        result = {"result": "OK", "content": []}
        user_list = CtrlUser().get_super_pl_and_pl()
        if user_list:
            result["result"] = "OK"
            result["content"] = user_list
        return result

    @auth.login_required
    def post(self):
        result = {"result": "NG", "error": ""}
        data_json = request.get_json(force=True)
        flag, msg = CtrlUser().update_pl_user(data_json)
        if flag:
            result["result"] = "OK"
            result["content"] = msg
        else:
            result["error"] = msg
        return result


class ApiProjUserRole(Resource):
    @auth.login_required
    def get(self, user_id, proj_id=None):
        result = {"result": "OK", "content": []}
        user_list = CtrlUser().get_user_roles(user_id, proj_id)
        if user_list:
            result["result"] = "OK"
            result["content"] = user_list
        return result

