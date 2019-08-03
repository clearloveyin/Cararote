from flask_restful import Resource, request
from app.api_1_0.api_base import set_result_code
from app.service.service_project import ServiceProject


class ApiProject(Resource):
    def get(self, proj_id=None):
        """获取所有项目"""
        if not proj_id:
            result = ServiceProject().get_all_project()
        else:
            result = ServiceProject().get_one_project(proj_id)
        set_result_code(result)
        return result

    def post(self):
        """添加一个项目"""
        request_data = request.get_json(force=True)
        result = ServiceProject().add_project(request_data)
        set_result_code(result)
        return result

    def put(self):
        """编辑项目信息"""
        request_data = request.get_json(force=True)
        result = ServiceProject().edit_project_data(request_data)
        set_result_code(result)
        return result