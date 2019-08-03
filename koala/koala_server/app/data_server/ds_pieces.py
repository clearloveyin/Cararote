import pandas as pd
import numpy as np
from app.db import cache, db
from app.db.users import Group, UserRole
SGL_ROLE_ID = 2
"""
一些零碎数据的cache，写在这个文件。
"""


@cache.memoize(timeout=3600 * 12)  # 12小时
def get_group_df():
    """获取组信息
    :return: Group Data Frame
    """
    print('*****************Reload Group Info.****************\n')
    q = (db.session.query(Group).filter(Group.group_id != 1).order_by(Group.group_name))
    group_df = pd.read_sql(q.statement, db.session.bind)
    return group_df


@cache.memoize(timeout=3600 * 12)  # 12小时
def get_gl_sgl_df(proj_id):
    """
    获取所有的GL组的父级关系信息信息
    :return:
    """
    print('*****************Reload GL Group Info.****************\n')
    sqlcmd = """
        SELECT t1.group_id, t1.group_name, 
        t2.group_id as parent_group_id, 
        t2.group_name as parent_group_name
        FROM public."group" as t1 left join public."group" as t2
        on t1.parent_group_id = t2.group_id
        WHERE t1.group_id in (	
            SELECT public."group".group_id FROM public."group"
            LEFT JOIN public.user_role
            ON  public."group".group_id = public.user_role.group_id
            WHERE proj_id = {proj_id} AND public."group".group_id not in( 
                select parent_group_id FROM public."group"
            )AND parent_group_id != 1
        )
    """.format(proj_id=proj_id)
    gl_sgl_df = pd.read_sql(sqlcmd, db.session.bind)
    gl_sgl_df[Group.group_id.name] = gl_sgl_df[Group.group_id.name].astype(np.float)
    return gl_sgl_df


def refresh_group_df():
    """刷新组信息的cache
    """
    cache.delete_memoized(get_group_df)
    cache.delete_memoized(get_gl_sgl_df)
    group_df = get_group_df()
    # gl_sgl_df = get_gl_sgl_df()
    return group_df



