"""empty message

Revision ID: 49c73192a415
Revises: 8103645bfc9c
Create Date: 2019-06-13 09:42:57.865343

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49c73192a415'
down_revision = '8103645bfc9c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('combination_car_id_fkey', 'combination', type_='foreignkey')
    op.drop_constraint('combination_proj_id_fkey', 'combination', type_='foreignkey')
    op.drop_constraint('combination_destination_id_fkey', 'combination', type_='foreignkey')
    op.create_foreign_key(None, 'combination', 'destination', ['destination_id'], ['destination_id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'combination', 'car', ['car_id'], ['car_id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'combination', 'project', ['proj_id'], ['proj_id'], source_schema='public', referent_schema='public')
    op.drop_constraint('project_update_user_fkey', 'project', type_='foreignkey')
    op.drop_constraint('project_create_user_fkey', 'project', type_='foreignkey')
    op.create_foreign_key(None, 'project', 'users', ['update_user'], ['user_id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'project', 'users', ['create_user'], ['user_id'], source_schema='public', referent_schema='public')
    op.drop_constraint('project_roles_user_id_fkey', 'project_roles', type_='foreignkey')
    op.drop_constraint('project_roles_role_id_fkey', 'project_roles', type_='foreignkey')
    op.drop_constraint('project_roles_proj_id_fkey', 'project_roles', type_='foreignkey')
    op.create_foreign_key(None, 'project_roles', 'project', ['proj_id'], ['proj_id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'project_roles', 'users', ['user_id'], ['user_id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'project_roles', 'role', ['role_id'], ['role_id'], source_schema='public', referent_schema='public')
    op.drop_constraint('role_perm_rel_perm_id_fkey', 'role_perm_rel', type_='foreignkey')
    op.drop_constraint('role_perm_rel_role_id_fkey', 'role_perm_rel', type_='foreignkey')
    op.create_foreign_key(None, 'role_perm_rel', 'permission', ['perm_id'], ['perm_id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'role_perm_rel', 'role', ['role_id'], ['role_id'], source_schema='public', referent_schema='public')
    op.drop_constraint('feature_create_user_fkey', 'feature', schema='func', type_='foreignkey')
    op.drop_constraint('feature_update_user_fkey', 'feature', schema='func', type_='foreignkey')
    op.create_foreign_key(None, 'feature', 'users', ['update_user'], ['user_id'], source_schema='func', referent_schema='public')
    op.create_foreign_key(None, 'feature', 'users', ['create_user'], ['user_id'], source_schema='func', referent_schema='public')
    op.drop_constraint('feature_func_proj_id_fkey', 'feature_func', schema='func', type_='foreignkey')
    op.create_foreign_key(None, 'feature_func', 'project', ['proj_id'], ['proj_id'], source_schema='func', referent_schema='public')
    op.drop_constraint('proj_catalog_proj_id_fkey', 'proj_catalog', schema='func', type_='foreignkey')
    op.create_foreign_key(None, 'proj_catalog', 'project', ['proj_id'], ['proj_id'], source_schema='func', referent_schema='public')
    op.drop_constraint('proj_feature_proj_id_fkey', 'proj_feature', schema='func', type_='foreignkey')
    op.drop_constraint('proj_feature_creat_user_fkey', 'proj_feature', schema='func', type_='foreignkey')
    op.drop_constraint('proj_feature_update_user_fkey', 'proj_feature', schema='func', type_='foreignkey')
    op.create_foreign_key(None, 'proj_feature', 'users', ['creat_user'], ['user_id'], source_schema='func', referent_schema='public')
    op.create_foreign_key(None, 'proj_feature', 'project', ['proj_id'], ['proj_id'], source_schema='func', referent_schema='public')
    op.create_foreign_key(None, 'proj_feature', 'users', ['update_user'], ['user_id'], source_schema='func', referent_schema='public')
    op.drop_constraint('proj_feature_combination_combination_id_fkey', 'proj_feature_combination', schema='func', type_='foreignkey')
    op.create_foreign_key(None, 'proj_feature_combination', 'combination', ['combination_id'], ['combination_key'], source_schema='func', referent_schema='public')
    op.drop_constraint('proj_func_proj_id_fkey', 'proj_func', schema='func', type_='foreignkey')
    op.create_foreign_key(None, 'proj_func', 'project', ['proj_id'], ['proj_id'], source_schema='func', referent_schema='public')
    op.drop_constraint('rfq_proj_id_fkey', 'rfq', schema='func', type_='foreignkey')
    op.create_foreign_key(None, 'rfq', 'project', ['proj_id'], ['proj_id'], source_schema='func', referent_schema='public')
    op.drop_constraint('spec_catalog_update_user_fkey', 'spec_catalog', schema='func', type_='foreignkey')
    op.drop_constraint('spec_catalog_create_user_fkey', 'spec_catalog', schema='func', type_='foreignkey')
    op.create_foreign_key(None, 'spec_catalog', 'users', ['create_user'], ['user_id'], source_schema='func', referent_schema='public')
    op.create_foreign_key(None, 'spec_catalog', 'users', ['update_user'], ['user_id'], source_schema='func', referent_schema='public')
    op.add_column('spec_func', sa.Column('contents', sa.String(), nullable=True), schema='func')
    op.drop_constraint('spec_func_create_user_fkey', 'spec_func', schema='func', type_='foreignkey')
    op.drop_constraint('spec_func_update_user_fkey', 'spec_func', schema='func', type_='foreignkey')
    op.create_foreign_key(None, 'spec_func', 'users', ['update_user'], ['user_id'], source_schema='func', referent_schema='public')
    op.create_foreign_key(None, 'spec_func', 'users', ['create_user'], ['user_id'], source_schema='func', referent_schema='public')
    op.drop_column('spec_func', 'content', schema='func')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('spec_func', sa.Column('content', sa.VARCHAR(length=256), autoincrement=False, nullable=True), schema='func')
    op.drop_constraint(None, 'spec_func', schema='func', type_='foreignkey')
    op.drop_constraint(None, 'spec_func', schema='func', type_='foreignkey')
    op.create_foreign_key('spec_func_update_user_fkey', 'spec_func', 'users', ['update_user'], ['user_id'], source_schema='func')
    op.create_foreign_key('spec_func_create_user_fkey', 'spec_func', 'users', ['create_user'], ['user_id'], source_schema='func')
    op.drop_column('spec_func', 'contents', schema='func')
    op.drop_constraint(None, 'spec_catalog', schema='func', type_='foreignkey')
    op.drop_constraint(None, 'spec_catalog', schema='func', type_='foreignkey')
    op.create_foreign_key('spec_catalog_create_user_fkey', 'spec_catalog', 'users', ['create_user'], ['user_id'], source_schema='func')
    op.create_foreign_key('spec_catalog_update_user_fkey', 'spec_catalog', 'users', ['update_user'], ['user_id'], source_schema='func')
    op.drop_constraint(None, 'rfq', schema='func', type_='foreignkey')
    op.create_foreign_key('rfq_proj_id_fkey', 'rfq', 'project', ['proj_id'], ['proj_id'], source_schema='func')
    op.drop_constraint(None, 'proj_func', schema='func', type_='foreignkey')
    op.create_foreign_key('proj_func_proj_id_fkey', 'proj_func', 'project', ['proj_id'], ['proj_id'], source_schema='func')
    op.drop_constraint(None, 'proj_feature_combination', schema='func', type_='foreignkey')
    op.create_foreign_key('proj_feature_combination_combination_id_fkey', 'proj_feature_combination', 'combination', ['combination_id'], ['combination_key'], source_schema='func')
    op.drop_constraint(None, 'proj_feature', schema='func', type_='foreignkey')
    op.drop_constraint(None, 'proj_feature', schema='func', type_='foreignkey')
    op.drop_constraint(None, 'proj_feature', schema='func', type_='foreignkey')
    op.create_foreign_key('proj_feature_update_user_fkey', 'proj_feature', 'users', ['update_user'], ['user_id'], source_schema='func')
    op.create_foreign_key('proj_feature_creat_user_fkey', 'proj_feature', 'users', ['creat_user'], ['user_id'], source_schema='func')
    op.create_foreign_key('proj_feature_proj_id_fkey', 'proj_feature', 'project', ['proj_id'], ['proj_id'], source_schema='func')
    op.drop_constraint(None, 'proj_catalog', schema='func', type_='foreignkey')
    op.create_foreign_key('proj_catalog_proj_id_fkey', 'proj_catalog', 'project', ['proj_id'], ['proj_id'], source_schema='func')
    op.drop_constraint(None, 'feature_func', schema='func', type_='foreignkey')
    op.create_foreign_key('feature_func_proj_id_fkey', 'feature_func', 'project', ['proj_id'], ['proj_id'], source_schema='func')
    op.drop_constraint(None, 'feature', schema='func', type_='foreignkey')
    op.drop_constraint(None, 'feature', schema='func', type_='foreignkey')
    op.create_foreign_key('feature_update_user_fkey', 'feature', 'users', ['update_user'], ['user_id'], source_schema='func')
    op.create_foreign_key('feature_create_user_fkey', 'feature', 'users', ['create_user'], ['user_id'], source_schema='func')
    op.drop_constraint(None, 'role_perm_rel', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'role_perm_rel', schema='public', type_='foreignkey')
    op.create_foreign_key('role_perm_rel_role_id_fkey', 'role_perm_rel', 'role', ['role_id'], ['role_id'])
    op.create_foreign_key('role_perm_rel_perm_id_fkey', 'role_perm_rel', 'permission', ['perm_id'], ['perm_id'])
    op.drop_constraint(None, 'project_roles', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'project_roles', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'project_roles', schema='public', type_='foreignkey')
    op.create_foreign_key('project_roles_proj_id_fkey', 'project_roles', 'project', ['proj_id'], ['proj_id'])
    op.create_foreign_key('project_roles_role_id_fkey', 'project_roles', 'role', ['role_id'], ['role_id'])
    op.create_foreign_key('project_roles_user_id_fkey', 'project_roles', 'users', ['user_id'], ['user_id'])
    op.drop_constraint(None, 'project', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'project', schema='public', type_='foreignkey')
    op.create_foreign_key('project_create_user_fkey', 'project', 'users', ['create_user'], ['user_id'])
    op.create_foreign_key('project_update_user_fkey', 'project', 'users', ['update_user'], ['user_id'])
    op.drop_constraint(None, 'combination', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'combination', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'combination', schema='public', type_='foreignkey')
    op.create_foreign_key('combination_destination_id_fkey', 'combination', 'destination', ['destination_id'], ['destination_id'])
    op.create_foreign_key('combination_proj_id_fkey', 'combination', 'project', ['proj_id'], ['proj_id'])
    op.create_foreign_key('combination_car_id_fkey', 'combination', 'car', ['car_id'], ['car_id'])
    # ### end Alembic commands ###
