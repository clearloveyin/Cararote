from flask_restful import Resource, request
from app.service.service_user import ServiceUser
from app.api_1_0.api_base import set_result_code


class Root(Resource):
    def get(self):
        return "This is Spider Server."


class Login(Resource):
    def post(self):
        """登录走cactus的工号登录"""
        request_data = request.get_json(force=True)
        result = ServiceUser().login_from_ldap(request_data)
        set_result_code(result)
        return result



