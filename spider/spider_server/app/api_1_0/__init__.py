from flask_restful import Resource
from app.api_1_0.api_login import Login
from app.api_1_0.api_feature_import import ApiFeatureImport
from app.api_1_0.api_project import ApiProject
from app.api_1_0.api_user import ApiUser, ApiRole


class Root(Resource):
    def get(self):
        return "This is spider Server."

class Api_1_0():
    def __init__(self, api):
        # Home
        api.add_resource(Root, '/')
        # 登录
        api.add_resource(Login, '/login')
        # feature初版本导入
        api.add_resource(ApiFeatureImport, '/feature/import')
        # Project
        api.add_resource(ApiProject, '/project/add', # 添加
                                     '/project/list', # 获取项目列表
                                     '/project/<int:proj_id>', # 获取单个项目的信息
                                     '/project/edit' # 编辑
                         )
        # User,Role,Permission
        api.add_resource(ApiUser, '/user/list')
        api.add_resource(ApiRole, '/role/list')

