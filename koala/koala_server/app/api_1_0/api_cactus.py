import json
from requests import get, put, post, delete
from flask import current_app


class ApiCactus(object):
    def __init__(self):
       pass

    def cactus_login(self, employ):
        r = post(current_app.config["LOGIN_URL"], employ)
        user_dict = dict()
        if r.status_code == 200:  # 成功
            result = json.loads(r.content)
            if result.get("code") == 0:  # 表示成功
                accessToken = result.get("info").get("accessToken")
                refreshToken = result.get("info").get("refreshToken")
                username = result.get("info").get("userName")
                work_id = result.get("info").get("employeeNo")
                user_dict = {'username': username, "accessToken": accessToken, "work_id": work_id}
        return user_dict

    def cactus_project(self, accessToken):
        headers = {"authToken": accessToken,
                   "Content-Type": "application/x-www-form-urlencoded"}
        proj_info = {"searchWord": ""}  # {"searchWord": "P1001"}
        r = post(current_app.config["PROJ_URL"], proj_info, headers=headers)
        result = dict()
        if r.status_code == 200:
            result = json.loads(r.content)
        return result

    def cactus_project_group(self, accessToken, minorProjectId):
        headers = {"authToken": accessToken,
                   "Content-Type": "application/json"}
        proj_group_info = {"minorProjectId": minorProjectId}
        s = json.dumps(proj_group_info)
        r = post(current_app.config["PROJECTGROUP_URL"], s, headers=headers)
        result = dict()
        if r.status_code == 200:
            result = json.loads(r.content)
        return result
