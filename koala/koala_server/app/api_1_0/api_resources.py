# -*- coding: UTF-8 -*-
from app.ctrl.ctrl_resources import CtrlResources
from flask_restful import Resource, request
from token_manage import auth


class ApiInputUpload(Resource):
    @auth.login_required
    def post(self):
        result = {"result": "NG"}
        data = request
        if data:
            if data.form.get("type") == "FILE":
                succsee, message = CtrlResources().import_file(data)
            else:
                succsee, message = CtrlResources().import_txt(data)
            if succsee:
                result = {"result": "OK"}
            else:
                result["error"] = message
        else:
            result["error"] = "请不要传空数据"
        return result

    @auth.login_required
    def get(self, quotation_id):
        result = {"result": "NG", "content": []}
        res, msg = CtrlResources().get_input_by_quotation_id(quotation_id)
        if res:
            result["result"] = "OK"
            result["content"] = msg
        else:
            result["error"] = msg
        return result


class ApiInputInfo(Resource):
    @auth.login_required
    def get(self, proj_id, _type):
        result = {"result": "NG", "content": []}
        res, msg = CtrlResources().get_input_by_proj_id(proj_id, _type)
        if res:
            result["result"] = "OK"
            result["content"] = msg
        else:
            result["error"] = msg
        return result


class ApiInputDel(Resource):
    @auth.login_required
    def post(self):
        json_data = request.get_json(force=True)
        resource_id = json_data.get('resource_id')
        resource_data_id = json_data.get('resource_data_id')
        result = {"result": "NG", "content": []}
        res, msg = CtrlResources().del_input(resource_id, resource_data_id)
        if res:
            result["result"] = "OK"
            result["content"] = msg
        else:
            result["content"] = msg
        return result

    @auth.login_required
    def get(self, resource_id, resource_data_id):
        result = {"result": "NG", "content": []}
        # res, msg = CtrlResources().del_input(resource_id, resource_data_id)
        # if res:
        #     result["result"] = "OK"
        #     result["content"] = msg
        # else:
        #     result["content"] = msg
        return result
