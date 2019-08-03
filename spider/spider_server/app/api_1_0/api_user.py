from flask_restful import Resource
from app.api_1_0.api_base import set_result_code
from app.service.service_user import ServiceUser


class ApiUser(Resource):
    def get(self):
        """获取所有项目"""
        result = ServiceUser().get_user_list()
        set_result_code(result)
        return result


class ApiRole(Resource):
    def get(self):
        """获取所有角色"""
        result = ServiceUser().get_role_list()
        set_result_code(result)
        return result