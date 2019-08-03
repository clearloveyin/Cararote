import json
import ldap
from flask import g
from flask import current_app
from requests import post
from ..service import *
from token_manage import serializer
from app.db import db
from app.controller.ctrl_user import CtrlUser
ldapServer = 'LDAP://apolo.storm'
domain = 'storm'



class ServiceUser(object):
    def __init__(self):
        self.ctrl_object = CtrlUser()

    def login_from_ldap(self, request_data):
        """
        登录走strom账号
        :param username:
        :param password:
        :return:
        """
        ctrl_object = self.ctrl_object
        result = {"type": SUCCESS, "content": None}
        username = request_data.get("username")
        password = request_data.get("password")
        if not username or not password:
            result["type"] = PROMPT_ERROR
            message = "工号和密码不能为空！"
            current_app.logger.info(message)
            result["message"] = message
            return result
        res = self.login_check(username, password)
        if res:
            try:
                user = ctrl_object.add_new_user(username)
                g.username = username
                g.password = password
                token = serializer.dumps({'username': username})
                user['LoginToken'] = str(token, encoding='utf-8')
                result["content"] = user
                db.session.commit()
                return result
            except Exception as e:
                db.session.rollback()
                result = return_exception_message(e)
                return result
        else:
            result["type"] = PROMPT_ERROR
            message = "登录失败，请输入正确的用户名或密码！"
            current_app.logger.info(message)
            result["message"] = message
            return result

    def login_check(self, username, password):
        try:
            conn = ldap.initialize(ldapServer)
            domainUserName = domain + '\\' + username
            conn.simple_bind_s(domainUserName, password)
            return True
        except:
            return False

    def login_from_cactus(self, request_data):
        """
        登录走cactus
        :param work_id:
        :param password:
        :return:
        """
        ctrl_object = self.ctrl_object
        work_id = request_data.get("username")
        password = request_data.get("password")
        employ = {"employeeNo": work_id,
                  "password": password,
                  "clientType": 0
                  }
        result = {"type": SUCCESS, "content": None}
        if not work_id or not password:
            result["type"] = PROMPT_ERROR
            message = "工号和密码不能为空！"
            current_app.logger.info(message)
            result["message"] = message
            return result
        try:
            user_dict = self.post_cactus(employ)
            if user_dict:
                username = user_dict.get('username')
                work_id = user_dict.get("work_id")
                user = ctrl_object.register(username=username, work_id=work_id)
                g.username = work_id
                g.password = password
                token = serializer.dumps({'username': username})
                user['LoginToken'] = str(token, encoding='utf-8')
                result["content"] = user
                return result
            else:
                result["type"] = PROMPT_ERROR
                message = "登录失败，请输入正确的用户名或密码！"
                current_app.logger.info(message)
                result["message"] = message
                return result
        except Exception as e:
            db.session.rollback()
            result = return_exception_message(e)
            return result

    def post_cactus(self, employ):
        login_post = current_app.config["LOGIN_URL"]
        r = post(login_post, employ, timeout=30)
        user_dict = dict()
        if r.status_code == 200:  # 成功
            result = json.loads(r.content)
            if result.get("code") == 0:  # 表示成功
                # accessToken = result.get("info").get("accessToken")
                username = result.get("info").get("userName")
                work_id = result.get("info").get("employeeNo")
                user_dict = {'username': username, "work_id": work_id}
        return user_dict

    def get_user_list(self):
        """获取所有的用户"""
        ctrl_object = self.ctrl_object
        result = {"type": SUCCESS, "content": None}
        try:
            user_list = ctrl_object.get_all_users()
            if not user_list:
                result["type"] = NOT_DATA
                message = "暂无用户！"
                result["message"] = message
            else:
                result["content"] = user_list
            return result
        except Exception as e:
            result = return_exception_message(e)
            return result

    def get_role_list(self):
        """获取所有的角色"""
        ctrl_object = self.ctrl_object
        result = {"type": SUCCESS, "content": None}
        try:
            role_list = ctrl_object.get_all_roles()
            if not role_list:
                result["type"] = NOT_DATA
                message = "暂无用户！"
                result["message"] = message
            else:
                result["content"] = role_list
            return result
        except Exception as e:
            result = return_exception_message(e)
            return result

