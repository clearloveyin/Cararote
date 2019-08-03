from flask_restful import Resource, request
from flask import after_this_request
from token_manage import auth
from flask import current_app, send_from_directory
from app.ctrl.ctrl_cost import CtrlCost
import os


class ApiCost(Resource):
    @auth.login_required
    def get(self, quotation_id, user_id, myself=None):
        result = {"result": "NG", "content": []}
        res, msg = CtrlCost().get_quotations_cost(quotation_id, user_id, myself)
        if res:
            result["result"] = "OK"
            result["content"] = msg
        else:
            result["error"] = msg
        return result

    @auth.login_required
    def post(self):
        result = {"result": "NG", "error": ""}
        data_json = request.get_json(force=True)
        res, msg = CtrlCost().update_cost(data_json)
        if res:
            result["result"] = "OK"
        else:
            result["error"] = msg
        return result


class ApiTaskCostHistiry(Resource):
    @auth.login_required
    def get(self, task_id):
        result = {"result": "NG", "content": []}
        res, msg = CtrlCost().get_task_cost_history(task_id)
        if res:
            result["result"] = "OK"
            result["content"] = msg
        else:
            result["error"] = msg
        return result


class ApiCostSummary(Resource):
    @auth.login_required
    def get(self, quotation_id, user_id):
        result = {"result": "NG", "content": []}
        res, msg = CtrlCost().summary_cost(quotation_id, user_id)
        if res:
            result["result"] = "OK"
            result["content"] = res
        else:
            result["error"] = msg
        return result


class ApiCostDetail(Resource):
    @auth.login_required
    def get(self, func_id):
        result = {"result": "NG", "content": []}
        res, msg = CtrlCost().get_detail_cost(func_id)
        if res:
            result["result"] = "OK"
            result["content"] = msg
        else:
            result["error"] = msg
        return result


class ExportSummary(Resource):
    @auth.login_required
    def get(self, user_id, quotation_id, unit):
        result = {"result": "OK", "content": '', 'error': ''}
        if quotation_id:
            res, path = CtrlCost().export_cost_summary_info(quotation_id, user_id, unit)
            if res:
                result["result"] = "OK"
                result["content"] = path
            else:
                result["content"] = ''
        return result


class ApiDownLoad(Resource):
    # @auth.login_required
    def get(self, path):
        file_name = os.path.basename(path)
        path_info = path.replace(file_name, '')
        current_app.logger.info('DownLoad file path=%s, %s' %
                                (os.path.join('../', path_info), file_name))
        data = send_from_directory(os.path.join('../', path_info), file_name, as_attachment=True)
        @after_this_request
        def remove_file(response):
            import platform
            file_path = path_info.strip('/')
            if platform.system() == 'Windows':
                os.system("rd/s/q  %s"%file_path)
            else:
                import shutil
                shutil.rmtree(file_path)
            return response
        return data

