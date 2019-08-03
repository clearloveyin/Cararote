from ..db import db
from sqlalchemy.orm import relationship
from sqlalchemy.schema import CreateSequence, Sequence


CreateSequence(Sequence('test_seq'))


class UserRole(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'user_role'

    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('public.roles.role_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('public.users.user_id'))
    proj_id = db.Column(db.Integer, db.ForeignKey('func.projects.proj_id'))
    group_id = db.Column(db.Integer, db.ForeignKey('public.group.group_id'))

    def __repr__(self):
        return '<UserRole role_id:%r, user_id:%r' % (self.role_id, self.user_id)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


db.Index('public_user_role_project_group_user_id_idx',
         UserRole.proj_id, UserRole.group_id,
         UserRole.user_id,
         unique=True
         )


role_perm = db.Table('role_permission',
                     db.Column('id', db.Integer, primary_key=True),
                     db.Column('role_id', db.Integer, db.ForeignKey('public.roles.role_id')),
                     db.Column('perm_id', db.Integer, db.ForeignKey('public.permission.permission_id')))

# user_role = db.Table('user_role',
#                      db.Column('id', db.Integer, primary_key=True),
#                      db.Column('user_id', db.Integer, db.ForeignKey('public.users.user_id')),
#                      db.Column('role_id', db.Integer, db.ForeignKey('public.roles.role_id')),
#                      db.Column('group_id', db.Integer, db.ForeignKey('public.group.group_id')),
#                      db.Column('proj_id', db.Integer, db.ForeignKey('func.projects.proj_id')))
# class RolePermission(db.Model):
#     __table_args__ = {"schema": "public"}
#     __tablename__ = 'role_permission'
#
#     id = db.Column(db.Integer, primary_key=True)
#     permission_id = db.Column(db.Integer, db.ForeignKey('public.permission.permisssion_id'))
#     role_id = db.Column(db.Integer, db.ForeignKey('public.roles.role_id'))
#
#     def to_dict(self):
#         d = {}
#         for column in self.__table__columns:
#             d[column.name] = getattr(self. column.name)
#         return d


class Permission(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'permission'

    permission_id = db.Column(db.Integer, primary_key=True)
    permission_name = db.Column(db.String(100))
    module_name = db.Column(db.String(100))

    def __repr__(self):
        return '<Permission permission_if:%r, permission_name:%r' % (self.permission_id, self.permission_name)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class Roles(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'roles'

    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(100))
    describe = db.Column(db.String(500))
    permissions = db.relationship('Permission', secondary=role_perm, backref=db.backref('roles'))

    def __repr__(self):
        return '<Role %r>' % self.role_name

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class Users(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    work_id = db.Column(db.String(100))  # 工号
    user_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    user_type = db.Column(db.String(50))  # 用户类型：TESE:后台测试账号； NORMAL:员工账号
    # roles = db.relationship('Roles', secondary=user_role, backref=db.backref('users'))

    # functions = relationship('Functions', backref='users')
    # # faults = relationship('Fault', backref='users')
    # input_resource_infos = relationship('InputResourceInfo', backref='users')

    observer = relationship('ProjectObserver', backref='users')
    projects = relationship('Projects', backref='users')
    # issues = relationship('Issue', backref='users')
    # replies = relationship('Reply', backref='users')

    def __repr__(self):
        return '<user_name:%r>' % self.user_name

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class Group(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'group'

    group_id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(100))
    describe = db.Column(db.String(1024))
    parent_group_id = db.Column(db.Integer)
    owner_user = db.Column(db.Integer, db.ForeignKey('public.users.user_id'))

    # func_man_days = relationship('FuncManDay', backref='group')
    # group_members = relationship('Users', secondary=user_role, backref='groups')

    def __repr__(self):
        return '<group describe:%r>' % self.describe

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


