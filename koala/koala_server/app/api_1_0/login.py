# -*- coding: UTF-8 -*-
from flask_restful import Resource, request
# import ldap
from flask import current_app
from flask import g
from token_manage import serializer
from app.ctrl.ctrl_user import CtrlUser
from .api_cactus import ApiCactus


class Root(Resource):
    def get(self):
        return "This is Koala Server."


class Login(Resource):

    def post(self):
        json_data = request.get_json(force=True)
        username = json_data.get('username')
        password = json_data.get('password')
        result = self.login_from_cactus(username, password)
        # user_obj = CtrlUser().get_user_by_work(username)
        # if user_obj:
        #     user_name = user_obj.user_name
        #     user = CtrlUser().register(username=user_name)
        #     result = {'result': "OK", 'accessToken': ''}
        #     result.update(user)
        # else:
        #     return {'result': "NG", "error": u'登录失败，请输入正确的用户名或密码！'}
        if result.get('result') == "OK":
            g.username = username
            g.password = password
            token = serializer.dumps({'username': username})
            result['LoginToken'] = str(token, encoding='utf-8')
        return result

    def get_password(self, username):
        user = CtrlUser().get_user_by_name(username)
        if user:
            if user.user_type == 'TEST':
                return user.password
        return None

    def login_from_cactus(self, work_id, password):
        """
        登录走cactus
        :param work_id:
        :param password:
        :return:
        """
        employ = {"employeeNo": work_id,
                  "password": password,
                  "clientType": 0
                  }
        user_dict = ApiCactus().cactus_login(employ)
        if user_dict:
            username = user_dict.get('username')
            accessToken = user_dict.get('accessToken')
            work_id = user_dict.get("work_id")
            user = CtrlUser().register(username=username, work_id=work_id)
            if user:
                result = {'result': "OK", 'accessToken': accessToken}
                result.update(user)
                return result
            else:
                current_app.logger.info("[注册用户失败], username=%s" % username)
                return {'result': "NG", "error": u'注册用户失败!'}
        else:
            return {'result': "NG", "error": u'登录失败，请输入正确的用户名或密码！'}

