from sqlalchemy.orm import aliased
from app.db import db
from app.controller.ctrl_base import CtrlBase
from app.db.project import Project, ProjectRoles
from app.db.user import Users


class CtrlProject(CtrlBase):
    def __init__(self):
        CtrlBase.__init__(self)
        self.project_model = Project
        self.project_features = []
        self.project_functions = []
        self.project_members = []

    def get_all_project(self):
        project_list = []
        CreateUser = aliased(Users)
        UpdateUser = aliased(Users)
        qs = (db.session.query(Project, CreateUser.user_name.label('create_user_name'),
                               UpdateUser.user_name.label('update_user_name'))
              .outerjoin(CreateUser, Project.create_user == CreateUser.user_id)
              .outerjoin(UpdateUser, Project.update_user == UpdateUser.user_id)
              .order_by(Project.proj_id))
        for q in qs:
            project_dict = dict()
            project_dict[Project.proj_id.name] = q.proj_id
            project_dict[Project.proj_name.name] = q.proj_name
            project_dict[Project.describe.name] = q.describe
            project_dict[Project.create_time.name] = q.create_time
            project_dict[Project.update_time.name] = q.update_time
            project_dict[Project.create_user.name] = q.create_user_name
            project_dict[Project.update_user.name] = q.update_user_name
            project_list.append(project_dict)
        return project_list

    def get_one_project(self, proj_id):
        CreateUser = aliased(Users)
        UpdateUser = aliased(Users)
        q = (db.session.query(Project, CreateUser.user_name.label('create_user_name'),
                              UpdateUser.user_name.label('update_user_name'))
              .outerjoin(CreateUser, Project.create_user == CreateUser.user_id)
              .outerjoin(UpdateUser, Project.update_user == UpdateUser.user_id)
              .filter(Project.proj_id == proj_id)
              .first())
        project_dict = dict()
        if q:
            project_dict[Project.proj_id.name] = q.proj_id
            project_dict[Project.proj_name.name] = q.proj_name
            project_dict[Project.describe.name] = q.describe
            project_dict[Project.create_time.name] = q.create_time
            project_dict[Project.update_time.name] = q.update_time
            project_dict[Project.create_user.name] = q.create_user_name
            project_dict[Project.update_user.name] = q.update_user_name
        return project_dict

    def add_project(self, proj_data):
        now_time = self.get_current_time()
        proj_data[Project.create_time.name] = now_time
        proj_data[Project.update_time.name] = now_time
        new_project = Project(**proj_data)
        db.session.add(new_project)
        db.session.flush()
        proj_id = new_project.proj_id
        return proj_id

    def edit_project(self, proj_data):
        proj_id = proj_data.get(Project.proj_id.name)
        q = db.session.query(Project).filter(Project.proj_id == proj_id).first()
        if q:
            q.update(proj_data)
            return True
        else:
            return False

    def add_project_role(self, proj_id, user_id, role_id):
        new_project_role = {
            ProjectRoles.user_id.name: user_id,
            ProjectRoles.proj_id.name: proj_id,
            ProjectRoles.role_id.name: role_id
        }
        db.session.add(ProjectRoles(**new_project_role))

    def edit_project_role(self, proj_id, user_id, role_id):
        q = (db.session.query(ProjectRoles)
             .filter(proj_id == proj_id)
             .filter(user_id == user_id)
             .first())
        if q:
            if role_id != q.role_id:
                q.role_id = role_id
        else:
            self.add_project_role(proj_id, user_id, role_id)

