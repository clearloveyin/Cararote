from flask_restful import Resource, request
from token_manage import auth
from flask import current_app
from app.ctrl.ctrl_task import CtrlTask


class ApiTask(Resource):
    @auth.login_required
    def get(self, quotation_id):
        # @TODO yuyin 以后可能加user_id过滤
        result = {"result": "OK"}
        res = CtrlTask().get_quotations_task(quotation_id)
        if res:
            result["result"] = "OK"
            result["content"] = res
        return result

    @auth.login_required
    def post(self):
        result = {"result": "NG", "error": ""}
        data_json = request.get_json(force=True)
        res, msg = CtrlTask().update_task(data_json)
        if res:
            result["result"] = "OK"
        else:
            result["error"] = msg
        return result


class ApiCheckTaskDelete(Resource):
    @auth.login_required
    def get(self, quotation_id, commit_user, task_id):
        result = {"result": "NG", "error": ""}
        res, msg = CtrlTask().check_delete_task(quotation_id, commit_user, task_id)
        if res:
            result["result"] = "OK"
            result["error"] = msg
        else:
            result["error"] = msg
        return result
