# -*- coding: UTF-8 -*-
from flask_restful import Resource, request
from token_manage import auth
from flask import current_app
from app.ctrl.ctrl_quotations import CtrlQuotations


class ApiQuotations(Resource):
    @auth.login_required
    def put(self, quotation_id):
        """
        修改报价
        :return:
        """
        result = {"result": "NG", "content": []}
        data = request.get_json(force=True)
        if data:
            res, msg = CtrlQuotations().update_one_quotation_info(quotation_id, data)
            if res:
                result["result"] = "OK"
                result["content"] = msg
            else:
                result["error"] = msg
        return result

    @auth.login_required
    def get(self, quotation_id):
        """
        查看报价
        :return:
        """
        result = {"result": "NG", "content": []}
        if quotation_id:
            res, msg = CtrlQuotations().get_one_quotation_info(quotation_id)
            if res:
                result["result"] = "OK"
                result["content"] = msg
            else:
                result["error"] = msg
        return result


class ApiQuotationInfo(Resource):
    @auth.login_required
    def post(self):
        """
        发起报价
        :return:
        """
        result = {"result": "NG"}
        data = request.get_json(force=True)
        if data:
            succsee, message = CtrlQuotations().add_quotation(data)
            if succsee:
                result = {"result": "OK", 'content': message}
            else:
                result["error"] = message
        else:
            result["error"] = "请不要传空数据"
        return result

    @auth.login_required
    def get(self, page=None, size=None, pro_id=None):
        """
        获取所有base版本
        :return:
        """
        result = {"result": "NG", "content": []}
        if pro_id:
            res, msg = CtrlQuotations().get_base_quotation_list(pro_id)
        elif page and size:
            res, msg = CtrlQuotations().get_all_quotation_list_by_page(page, size)
        else:
            res, msg = CtrlQuotations().get_all_quotation_list()
        if res:
            result["result"] = "OK"
            result["content"] = msg
        else:
            result["error"] = msg
        return result


class ApiQuotationStatue(Resource):
    @auth.login_required
    def post(self):
        """
        修改状态
        :return:
        """
        result = {"result": "NG"}
        data = request.get_json(force=True)
        if data:
            succsee, message = CtrlQuotations().update_quotation_status(data)
            if succsee:
                result = {"result": "OK", 'content': message}
            else:
                result["error"] = message
        else:
            result["error"] = "请不要传空数据"
        return result

    @auth.login_required
    def get(self, quotation_id):
        """
        获取状态
        :return:
        """
        result = {"result": "NG", "content": []}
        if quotation_id:
            res, msg = CtrlQuotations().show_one_quotation_status(quotation_id)
            if res:
                result["result"] = "OK"
                result["content"] = msg
            else:
                result["error"] = msg
        return result


class ApiQuotationList(Resource):
    @auth.login_required
    def get(self, page, size, pro_id=None, user_id=None,):
        result = {"result": "NG", "content": []}
        if user_id and (not pro_id):
            res, msg = CtrlQuotations().get_quotation_list_by_user_id_page(user_id, page, size)
        else:
            res, msg = CtrlQuotations().get_quotation_list2_by_size(pro_id, user_id, page, size)
        if res:
            result["result"] = "OK"
            result["content"] = msg
        else:
            result["error"] = msg
        return result


class ApiOptionInfo(Resource):
    @auth.login_required
    def post(self, quotation_id):
        """
        更新/添加此报价下的Option
        :return:
        """
        result = {"result": "NG"}
        data = request.get_json(force=True)
        # data = request.view_args
        if data:
            succsee, message = CtrlQuotations().add_option_by_quotation_id2(quotation_id, data)
            if succsee:
                result = {"result": "OK", 'content': message}
            else:
                result["error"] = message
        else:
            result["error"] = "请不要传空数据"
        return result

    @auth.login_required
    def get(self, quotation_id):
        """
        获取此报价下的所有Option
        :return:
        """
        result = {"result": "OK", "content": []}
        if quotation_id:
            res = CtrlQuotations().get_option_by_quotation_id(quotation_id)
            if res:
                result["result"] = "OK"
                result["content"] = res

        return result


class ApiOptionValueInfo(Resource):
    @auth.login_required
    def post(self, option_id):
        """
        更新/添加此报价下的Option
        :return:
        """
        result = {"result": "NG"}
        # data = request.get_json(force=True)
        # if data:
        #     succsee, message = CtrlQuotations().update_option_by_quotation_id(option_id, data)
        #     if succsee:
        #         result = {"result": "OK", 'content': message}
        #     else:
        #         result["error"] = message
        # else:
        #     result["error"] = "请不要传空数据"
        return result

    @auth.login_required
    def get(self, option_id):
        """
        获取此报价下的所有Option
        :return:
        """
        result = {"result": "NG", "content": []}
        # if option_id:
        #     res, msg = CtrlQuotations().get_option_by_quotation_id(option_id)
        #     if res:
        #         result["result"] = "OK"
        #         result["content"] = msg
        #     else:
        #         result["content"] = msg
        return result


class ApiOptionCombinationInfo(Resource):
    @auth.login_required
    def post(self, quotation_id):
        """
        更新/添加此报价下的Combination
        :return:
        """
        result = {"result": "NG"}
        data = request.get_json(force=True)
        # data = request.view_args
        if data:
            succsee, message = CtrlQuotations().add_combination_by_quotation_id3(quotation_id, data)
            if succsee:
                result = {"result": "OK", 'content': message}
            else:
                result["error"] = message
        else:
            result["error"] = "请不要传空数据"
        return result

    @auth.login_required
    def get(self, quotation_id):
        """
        获取此报价下的所有Option
        :return:
        """
        result = {"result": "NG", "content": []}
        if quotation_id:
            res, msg = CtrlQuotations().get_combination_by_quotation_id3(quotation_id)
            if res:
                result["result"] = "OK"
                result["content"] = msg
            else:
                result["error"] = msg
        return result

    @auth.login_required
    def delete(self, op_id):
        """
        删除此条Option
        :return:
        """
        result = {"result": "NG", "content": []}
        if op_id:
            res, msg = CtrlQuotations().del_combination(op_id)
            if res:
                result["result"] = "OK"
                result["content"] = msg
            else:
                result["error"] = msg
        return result


class ApiFeatureInfo(Resource):
    @auth.login_required
    def post(self, quotation_id):
        """
        更新此报价下的feature
        :return:
        """
        result = {"result": "NG"}
        # data = request.get_json(force=True)
        # if data:
        #     succsee, message = CtrlQuotations().update_option_by_quotation_id(quotation_id, data)
        #     if succsee:
        #         result = {"result": "OK", 'content': message}
        #     else:
        #         result["error"] = message
        # else:
        #     result["error"] = "请不要传空数据"
        return result

    @auth.login_required
    def get(self, quotation_id, user_id):
        """
        获取此报价下的所有featureList
        :return:
        """
        result = {"result": "NG", "content": []}
        if quotation_id:
            res, msg = CtrlQuotations().get_feature_list2(quotation_id, user_id)
            if res:
                result["result"] = "OK"
                result["content"] = msg
            else:
                result["error"] = msg
        return result


class ApiFeatureImport(Resource):
    @auth.login_required
    def post(self):
        """
        更新此报价下的feature
        :return:
        """
        result = {"result": "NG"}
        request_data = request
        res, msg = CtrlQuotations().import_featurelist(request_data)
        if res:
            result["result"] = "OK"
            result["content"] = msg
        else:
            result["error"] = msg
        return result


class ApiFeatureAssign(Resource):
    @auth.login_required
    def post(self, quotation_id):
        """
        分配此报价下的feature
        :return:
        """
        result = {"result": "NG"}
        data = request.get_json(force=True)
        if data:
            succsee, message = CtrlQuotations().feature_assign_group(data, quotation_id)
            if succsee:
                result = {"result": "OK", 'content': message}
            else:
                result["error"] = message
        else:
            result["error"] = "请不要传空数据"
        return result

    @auth.login_required
    def get(self, quotation_id):
        """
        获取此报价下的featureList历史
        :return:
        """
        result = {"result": "NG", "content": []}
        if quotation_id:
            res, msg = CtrlQuotations().feature_history(quotation_id)
            if res:
                result["result"] = "OK"
                result["content"] = msg
            else:
                result["error"] = msg
        return result


class ApiQuotationPie(Resource):
    @auth.login_required
    def get(self, quotation_id):
        result = {"result": "NG", "content": []}
        res, msg = CtrlQuotations().get_quotation_pie(quotation_id)
        if res:
            result["result"] = "OK"
            result["content"] = msg
        else:
            result["error"] = msg
        return result
