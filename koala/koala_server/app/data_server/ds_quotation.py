import numpy as np
import pandas as pd
import re
from app.db import cache
from sqlalchemy_utils import refresh_materialized_view
from app.db.quotations import *
from app.db.users import *
from app.db.issues import Issue
from app.data_server.ds_pieces import get_group_df, get_gl_sgl_df


@cache.memoize(timeout=3600 * 12)  # 12小时
def get_ds_quotation(quotation_id):
    print('*****************Reload Quotation Data(quotation_id=%s)****************\n' % quotation_id)
    ds_q = DSQuotation(quotation_id)
    ds_q.load_function_task_manday_df()
    return ds_q


def refresh_ds_quotation(quotation_id=None):
    """刷新报价数据的cache
    @:param quotation_id: 报价ID
    """
    print('*****************Delete Quotation Cache(quotation_id=%s)****************\n' % quotation_id)
    if quotation_id:
        cache.delete_memoized_verhash(get_ds_quotation, quotation_id)
        ds_q = get_ds_quotation(quotation_id)
        return ds_q
    else:
        cache.delete_memoized_verhash(get_ds_quotation)
        return None


def refresh_lastest_man_day_id():
    """刷新最新工数ID的View
    :return:
    """
    refresh_materialized_view(db.session, 'lastest_man_day_id', concurrently=True)


def top(df, columns=None, n=1):
    """
    :param df: Data Frame.
    :param columns:排序字段
    :param n:取最大的几条
    :return:sub data frame: 只包含最大的几条
    """
    return df.sort_values(by=columns)[-n:]


def fun(x, major_func_ids, minor_func_ids):
    if x in major_func_ids:
        return "major"
    elif x in minor_func_ids:
        return "minor"
    else:
        return "nothing"


class DSQuotation(object):
    """报价数据服务
    """
    def __init__(self, quotation_id):
        self.quotation_id = quotation_id
        self.func_df = None
        self.task_df = None
        self.manday_df = None
        self.func_task_df = None
        self.category_df = None
        self.pre_df = None
        self.status_df = None
        self.option_df = None
        self.func_group_df = None
        self.func_columns = []
        self.task_columns = []

    def get_func_df(self, no_date=True):
        if no_date:
            return self.func_df.drop([Functions.create_time.name,
                                      Functions.update_time.name],
                                     axis=1)
        return self.func_df

    def get_task_df(self, no_date=True):
        if no_date:
            return self.task_df.drop([Task.create_time.name,
                                      Task.update_time.name],
                                     axis=1)
        return self.task_df

    def get_func_task_df(self):
        return self.func_task_df

    def get_func_column_num(self, func_df=None):
        if func_df is None:
            return len(self.func_columns)
        else:
            return len(self._get_func_columns(func_df))

    def get_task_column_num(self, task_df=None):
        if task_df is None:
            return len(self.task_columns)
        else:
            return len(self._get_task_columns(task_df))

    def get_func_columns(self, func_df=None):
        if func_df is None:
            return self.func_columns
        else:
            return self._get_func_columns(func_df)

    def get_task_columns(self, task_df=None):
        if task_df is None:
            return self.task_columns
        else:
            return self._get_task_columns(task_df)

    def get_diff_color_func(self, my_group_ids):
        """
        用relation字段来区分某个sgl主担当的feature以及关联的feature
        major是我担当的；minor是我关联的；nothing是跟我无关的
        :param my_group_id: 我的组id
        :return:
        """
        func_df = self.get_func_df()
        func_group_df = self.get_func_group_df()
        my_func_group = func_group_df[func_group_df[FuncGroup.group_id.name].isin(my_group_ids)]
        major_func_group = my_func_group[my_func_group[FuncGroup.group_role.name] == "major"]
        minor_func_group = my_func_group[my_func_group[FuncGroup.group_role.name] == "minor"]
        major_func_ids = major_func_group[FuncGroup.func_id.name].tolist()
        minor_func_ids = minor_func_group[FuncGroup.func_id.name].tolist()
        func_df["relation"] = func_df["func_id"].apply(lambda x: fun(x, major_func_ids, minor_func_ids))
        return func_df

    def get_diff_color_func_task(self, my_group_ids, my_role):
        """
        用relation字段来区分某个sgl/gl主担当的task以及关联的task
        major是我担当的；minor是我关联的；nothing是跟我无关的
        :param my_group_id: 我的组id
        :param my_role: 我的角色
        :return:
        """
        func_task_df = self.get_func_task_df()
        if my_role == "SGL":
            func_group_df = self.get_func_group_df()
            my_func_group = func_group_df[func_group_df[FuncGroup.group_id.name].isin(my_group_ids)]
            print(my_func_group)
            major_func_group = my_func_group[my_func_group[FuncGroup.group_role.name] == "major"]
            minor_func_group = my_func_group[my_func_group[FuncGroup.group_role.name] == "minor"]
            major_func_ids = major_func_group[FuncGroup.func_id.name].tolist()
            minor_func_ids = minor_func_group[FuncGroup.func_id.name].tolist()
            func_task_df["relation"] = func_task_df["func_id"].apply(lambda x: fun(x, major_func_ids, minor_func_ids))
        elif my_role == "GL":
            func_task_df["relation"] = func_task_df["group_id"].apply(lambda x:
                                                                      "major" if x in my_group_ids else "nothing")
        return func_task_df

    def load_function_task_manday_df(self):
        """获取function(feature list)/task和const的Data Frame."""
        self.load_function_df()
        self.load_task_df()
        func_df = self.get_func_df()
        task_df = self.get_task_df()
        self.func_task_df = self.merge_func_task(func_df, task_df)
        self.load_tasks_manday_df()
        # self.load_quotation_option()  # 加载option
        self.load_pre_df()  # 加载前提
        self.merge_manday_pre()  # 合并前提
        self.load_status_df()  # 加载状态
        self.merge_manday_status()  # 合并状态
        lastest_issus_df = self.load_lastest_issus_df()  # 加载指摘
        self.merge_manday_issus(lastest_issus_df)  # 合并指摘
        self.load_func_group_df()

    def load_function_df(self):
        """获取function(feature list)/task和const的Data Frame."""
        # q = (db.session.query(Functions).filter(Functions.quotation_id == quotation_id).order_by(Functions.order_id))
        q = (db.session.query(Functions)
             .filter(Functions.quotation_id == self.quotation_id)
             .order_by(Functions.order_id)
             )
        statement = q.statement
        self.func_df = pd.read_sql(statement, db.session.bind)
        self.load_category_df()
        self.merge_func_category()
        # ## 删除空列
        subset = self._get_func_columns(self.func_df)
        self.drop_na_columns(self.func_df, subset)
        self.func_columns = self._get_func_columns(self.func_df)
        self.func_df[Functions.func_id.name] = self.func_df[Functions.func_id.name].astype(np.int)

    def load_task_df(self):
        func_ids = [int(n) for n in list(self.func_df[Functions.func_id.name].unique())]
        q = (db.session.query(Task)
             .filter(Task.func_id.in_(func_ids))
             .filter(Task.delete == False)
             .order_by(Task.task1, Task.task2, Task.task3,
                       Task.task4, Task.task5, Task.task6)
             )
        # print(q.statement)
        self.task_df = pd.read_sql(q.statement, db.session.bind)
        subset = self._get_task_columns(self.task_df)
        self.drop_na_columns(self.task_df, subset)
        # print(self.task_df.columns)
        self.task_columns = self._get_task_columns(self.task_df)  # 剩下的Task列
        self.task_df[Task.task_id.name] = self.task_df[Task.task_id.name].astype(np.int)

    def drop_na_columns(self, df, subset):
        for col in subset:
            s = df[col]
            if not s.empty:
                if s.isnull().all():
                    df.drop([col], axis=1, inplace=True)
            else:
                df.drop([col], axis=1, inplace=True)

    def load_tasks_manday_df(self):
        task_ids = [int(n) for n in list(self.task_df[Task.task_id.name].unique())]
        if task_ids:
            self.manday_df = self._load_tasks_manday_df(task_ids)
            self.manday_df[FuncManDay.status_id.name].fillna(0, inplace=True)
            self.manday_df[FuncManDay.pre_id.name].fillna(0, inplace=True)
        else:
            self.manday_df = self._load_tasks_manday_df([0])
            # print(self.manday_df[FuncManDay.pre_id.name])

    def _get_func_columns(self, df, sub_str='sub'):
        func_columns = self._search_columns(df, sub_str)
        return func_columns

    def _get_task_columns(self, df, sub_str='task'):
        task_columns = self._search_columns(df, sub_str)
        return task_columns

    def _search_columns(self, df, sub_str):
        func_columns = []
        p = re.compile(r'^%s\d+' % sub_str)
        columns = list(df.columns)
        for column in columns:
            match = p.search(column)
            if match:  # sub1~N
                func_columns.append(column)
        return func_columns

    def _load_tasks_manday_df(self, task_ids):
        """获取Task的工数"""
        statement = """
        select t2.id, t2.base_id,
               t2.task_id, t2.option_id, t2.group_id,
               t2.version, t2.assin_to, status_id,
               days, pre_id, comment
          from lastest_man_day_id as t1
          left join func.func_man_day as t2
          on t1.option_id = t2.option_id and
             t1.group_id = t2.group_id and
             t1.task_id = t2.task_id and
             t1.lastet_ver_id = t2.version
          where t2.task_id in ({})
        """.format(', '.join([str(n) for n in task_ids]))
        manday_df = pd.read_sql(statement, db.session.bind,
                                index_col=["group_id", "option_id", "task_id"])
        return manday_df

    def _load_tasks_manday_df2(self, task_ids):
        """获取Task的工数"""
        q = (db.session.query(FuncManDay.id, FuncManDay.base_id, FuncManDay.task_id,
                              FuncManDay.group_id, FuncManDay.option_id, FuncManDay.status_id,
                              FuncManDay.days, FuncManDay.pre_id, FuncManDay.comment,
                              FuncManDay.version)
             .filter(FuncManDay.task_id.in_(task_ids)))
        all_manday_df = pd.read_sql(q.statement, db.session.bind)
        grouped = all_manday_df.groupby(by=[FuncManDay.group_id.name,
                                            FuncManDay.option_id.name,
                                            FuncManDay.task_id.name])
        # TODO@hcz: 这个地方性能有点慢
        manday_df = grouped.apply(top, columns=FuncManDay.version.name, n=1)
        # print(manday_df)
        return manday_df

    def get_manday_by_group_ids(self, group_ids):
        """
        :param group_ids: 组
        :return: 通过组list过滤的工数 DataFrame.
        """
        if not group_ids:
            return self.manday_df
        # print(self.manday_df)
        if self.manday_df is None:
            return None
        # print(self.manday_df)
        filter_df = self.manday_df.loc[(tuple(group_ids), ), :]
        # print(filter_df)
        # pd.DataFrame().unstack(level=[1, 2])
        return filter_df

    def get_manday_by_task_ids(self, task_ids):
        """
        :param task_ids:  task
        :return: 通过task_ids过滤 DataFrame
        """
        if not task_ids:
            return self.manday_df
        if self.manday_df is None:
            return None
        filter_df = self.manday_df.loc[(slice(None), slice(None), tuple(task_ids)), :]
        # print(filter_df)
        return filter_df

    def merge_func_task(self, func_df, task_df):
        """合并Function/Feature和Task
        :param func_df: Function DataFrame
        :param task_df: Task DataFrame
        :return: Merged DataFrame
        """
        merged_df = pd.merge(func_df, task_df,
                             left_on=Functions.func_id.name,
                             right_on=Task.func_id.name,
                             how='left'
                             )
        merged_df[Task.group_id.name] = merged_df[Task.group_id.name].replace([None], np.NaN)
        return merged_df

    def filter_and_split_manday_df(self, group_ids, parent_sub_group_ids, option_ids,
                                   manday_df=None, func_task_df=None, my=False,
                                   my_group_ids=None, my_role=None):
        """按group_ids过滤工数，再按option_id和group_id分割工数
        :param group_ids: 组列表
        :param option_ids: option list
        :param manday_df: DataFrame 工数信息
        :param func_task_df: Function/Feature Data frame
        :param my: my is True时，选择我的。过滤方法是:
                   Feature的主担当(GL：我的组，SGL: 我的组和我的所有小组)
                   or Task的主提当(GL：我的组，SGL: 我的组和我的所有小组)
                   or 工数 (GL：我的小组填的工数，SGL: 我的组填的工数和我的所有小组填的工数)
        :return: {(option_id1, group_id1): manday_df1,
                  (option_id2, group_id2): manday_df2,
                  ....
                 }
        """
        # 过滤组
        if manday_df is None:
            filter_manday_df = self.get_manday_by_group_ids(group_ids)
        else:
            filter_manday_df = manday_df
        if filter_manday_df is None:
            return dict()
        unstack_manday_df = filter_manday_df.unstack(level=[0, 1])  # 行转成列
        unstack_manday_df = unstack_manday_df.swaplevel(i=0, j=-1, axis=1)  # 字段和Option换一下
        if my:
            sub_manday_df = self._drop_empty_manday(unstack_manday_df)
            task_ids = list(sub_manday_df.index)
        else:
            task_ids = list(unstack_manday_df.index)
        if func_task_df is None or func_task_df.empty:
            func_task_df = self.get_func_task_df()
        if my:
            func_task_df = self._get_my_func_task(func_task_df, parent_sub_group_ids, task_ids)
            if not func_task_df.empty:
                # ## 删除Function/FeatureList空列
                # print(func_task_df.columns)
                subset = self._get_func_columns(func_task_df)
                self.drop_na_columns(func_task_df, subset)
                # print(func_task_df.columns)
                # ## 删除Task空列
                subset = self._get_task_columns(func_task_df)
                self.drop_na_columns(func_task_df, subset)
                # print(func_task_df.columns)
        # 按Task排序
        task_id_df = func_task_df[[Task.task_id.name]]
        if task_id_df[Task.task_id.name].is_unique:  # Task_id 是unique
            task_id_df.set_index(keys=[Task.task_id.name], inplace=True, drop=False)
            # 0, 0，在这里没有特别的意义，只是为会level对齐
            task_id_df.columns = pd.MultiIndex.from_tuples([(0, 0, 'task_id'), ], names=['option_id', 'group_id', 'manday'])
            sorted_df = pd.merge(task_id_df, unstack_manday_df,
                                 left_index=True, right_index=True, how='left', sort=False)
            # print(sorted_df)
        else:
            # 0, 0，在这里没有特别的意义，只是为会level对齐
            # print(task_id_df[Task.task_id.name])
            task_id_df.columns = pd.MultiIndex.from_tuples([(0, 0, 'task_id'), ],
                                                           names=['option_id', 'group_id', 'manday'])
            unstack_manday_df.index.name = (0, 0, "task_id")
            unstack_manday_df.reset_index(inplace=True)
            sorted_df = pd.merge(task_id_df, unstack_manday_df, how='left', sort=False)
            sorted_df.set_index((0, 0, "task_id"))
            sorted_df.index.name = "task_id"
            # print(sorted_df)
        option_group_dict = {}
        for option_id in option_ids:
            for group_id in group_ids:
                if (option_id, group_id) in sorted_df.columns:
                    option_group_df = sorted_df.loc[:, (option_id, group_id, slice(None))]
                    # print(option_group_df)
                    option_group_df.columns = option_group_df.columns.droplevel([0, 1])  # drop opttion_id, group_id
                    option_group_dict[(option_id, group_id)] = option_group_df.fillna('')
                else:
                    option_group_dict[(option_id, group_id)] = None
        return func_task_df, option_group_dict

    def _drop_empty_manday(self, unstack_manday_df):
        """去掉工数的空行
        :param unstack_manday_df:
        :return: sub_manday_df，没有空行的工数。
        """
        # option_ids = tuple(unstack_manday_df.columns.get_level_values(0))
        # group_ids = tuple(unstack_manday_df.columns.get_level_values(1))
        culs = (FuncManDay.days.name, FuncManDay.pre_id.name, FuncManDay.comment.name, FuncManDay.status_id.name)
        sub_manday_df = unstack_manday_df.loc[:, (slice(None), slice(None), culs)]
        # 去掉所有工数内容是空的行
        sub_manday_df = sub_manday_df.replace(0.0, np.NaN)
        sub_manday_df.replace('', np.NaN, inplace=True)
        sub_manday_df = sub_manday_df.dropna(how='all')
        return sub_manday_df

    def func_manday_detail(self, option_ids, func_id):
        """
        获取一条function下面的工数详细信息
        :param option_ids:
        :param func_id:
        :return:
        """
        task_df = self.get_func_task_df()
        filter_task_df = task_df[task_df[Task.func_id.name] == func_id]
        # ## 删除Task空列
        subset = self._get_task_columns(filter_task_df)
        self.drop_na_columns(filter_task_df, subset)
        task_ids = list(filter_task_df[Task.task_id.name])
        filter_manday_df = self.get_manday_by_task_ids(task_ids)
        if filter_manday_df is None:
            return dict()
        unstack_manday_df = filter_manday_df.unstack(level=[0, 1])  # 行转成列
        unstack_manday_df = unstack_manday_df.swaplevel(i=0, j=-1, axis=1)  # 字段和Option换一下
        sub_manday_df = self._drop_empty_manday(unstack_manday_df)
        manday_task_ids = list(sub_manday_df.index)
        # 筛选出有工数的task
        filter_task_df = filter_task_df[filter_task_df[Task.task_id.name].isin(manday_task_ids)]
        # 按Task排序
        task_id_df = filter_task_df[[Task.task_id.name]]
        # 0, 0，在这里没有特别的意义，只是为会level对齐
        # print(task_id_df[Task.task_id.name])
        task_id_df.columns = pd.MultiIndex.from_tuples([(0, 0, 'task_id'), ],
                                                       names=['option_id', 'group_id', 'manday'])
        unstack_manday_df.index.name = (0, 0, "task_id")
        unstack_manday_df.reset_index(inplace=True)
        # print(task_id_df)
        # print(unstack_manday_df)
        task_id_df[(0, 0, "task_id")] = task_id_df[(0, 0, "task_id")].astype(int)  # task_id转成int类型
        unstack_manday_df[(0, 0, "task_id")] = unstack_manday_df[(0, 0, "task_id")].astype(int)  # task_id转成int类型
        sorted_df = pd.merge(task_id_df, unstack_manday_df, how='right', sort=False)
        sorted_df.set_index((0, 0, "task_id"))
        sorted_df.index.name = "task_id"
        option_group_dict = dict()
        option_group_ids = []
        for option_id in option_ids:
            # print(unstack_manday_df.columns)
            manday_group_df = unstack_manday_df.loc[:, ((option_id,), )]
            group_ids = sorted(set(manday_group_df.columns.get_level_values(1)))
            option_group_ids.append(group_ids)
            for group_id in group_ids:
                option_group_df = sorted_df.loc[:, (option_id, group_id, slice(None))]
                # print(option_group_df)
                option_group_df.columns = option_group_df.columns.droplevel([0, 1])  # drop opttion_id, group_id
                option_group_dict[(option_id, group_id)] = option_group_df.fillna('')
        return filter_task_df, option_group_dict, option_group_ids

    def get_my_func_task(self, group_ids):
        filter_manday_df = self.get_manday_by_group_ids(group_ids)
        func_task_df = self.get_func_task_df()
        manday_df = filter_manday_df.reset_index(level=2)  # 释放task_id
        task_ids = list(manday_df.task_id)
        my_func_task = self._get_my_func_task(func_task_df, group_ids, task_ids)
        return my_func_task

    def _get_my_func_task(self, func_task_df, group_ids, task_ids):
        # print(func_task_df.columns)
        my_func_ids = self._get_my_funcs(group_ids)
        group_ids = set(group_ids)
        task_ids = set(task_ids)
        my_func_task_df = func_task_df[(func_task_df[Functions.func_id.name].isin(my_func_ids) |
                                        func_task_df[Task.group_id.name].isin(group_ids) |
                                        func_task_df[Task.task_id.name].isin(task_ids))]
        return my_func_task_df

    def _get_my_funcs(self, group_ids):
        my_func_df = self.func_group_df[self.func_group_df[FuncGroup.group_id.name].isin(group_ids)]
        return set(my_func_df[FuncGroup.func_id.name].unique())

    def merge_func_group_id(self, func_df, func_group_df):
        """
        :param func_df: Function/Feature Data Frame
        :param func_group_df:
        :return:
        """
        merged_df = pd.merge(func_df, func_group_df, on=Functions.func_id.name, how='left')
        # TODO@hcz: 空的group_id填成''
        merged_df[FuncGroup.group_id.name].fillna('', inplace=True)
        return merged_df

    def merge_func_group_name(self, func_df, func_group_df):
        """
        :param func_df: Function/Feature Data Frame
        :param func_group_df:
        :return:
        """
        # print(func_group_df)
        merged_df = pd.merge(func_df, func_group_df,
                             left_on=Functions.func_id.name,
                             right_index=True,
                             how='left')
        # TODO@hcz: 空的group_id填成''
        # print(merged_df)
        merged_df.fillna('', inplace=True)
        return merged_df

    def load_func_group_df(self):
        func_ids = [int(n) for n in list(self.func_df[Functions.func_id.name].unique())]
        q = (db.session.query(FuncGroup.func_id, FuncGroup.group_id, FuncGroup.group_role)
             .filter(FuncGroup.func_id.in_(func_ids))
             .order_by(FuncGroup.func_id)
             )
        self.func_group_df = pd.read_sql(q.statement, db.session.bind)

    def load_pre_df(self):
        """加载前提
        :return:
        """
        pre_id_ids = []
        if self.manday_df is None:
            return
        pre_id_s = (self.manday_df[FuncManDay.pre_id.name])
        pre_id_s = pre_id_s.fillna(0)
        s = pre_id_s.unique()
        pre_id_array = s[s != 0]
        pre_id_ids = [int(n) for n in list(pre_id_array) if n]
        q = (db.session.query(Preconditions.pre_id, Preconditions.precondition)
             .filter(Preconditions.pre_id.in_(pre_id_ids))
             .order_by(Preconditions.pre_id)
             )
        self.pre_df = pd.read_sql(q.statement, db.session.bind, index_col=Preconditions.pre_id.name)
        # self.pre_df.set_index(keys=Preconditions.precondition.name, drop=False)

    def merge_manday_pre(self):
        """
        :return:
        """
        # print(self.manday_df)
        self.manday_df = pd.merge(self.manday_df, self.pre_df,
                                  left_on=FuncManDay.pre_id.name,
                                  right_index=True,
                                  how='left')
        self.manday_df[Preconditions.precondition.name].fillna('', inplace=True)
        # print(self.manday_df)
        # pass

    def load_status_df(self):
        q = (db.session.query(FuncStatus.status_id, FuncStatus.status)
             .order_by(FuncStatus.status_id)
             )
        self.status_df = pd.read_sql(q.statement, db.session.bind, index_col=FuncStatus.status_id.name)
        # self.status_df.set_index(keys=FuncStatus.status.name, drop=False)

    def merge_manday_status(self):
        """
        :return:
        """
        # print(self.manday_df.columns)
        # print(self.status_df)
        # print(self.manday_df[FuncManDay.status_id.name])
        self.manday_df = pd.merge(self.manday_df, self.status_df,
                                  left_on=FuncManDay.status_id.name,
                                  right_index=True,
                                  how='left')
        self.manday_df[FuncStatus.status.name].fillna('', inplace=True)
        # print(self.manday_df)

    def load_category_df(self):
        category_ids = []
        for n in list(self.func_df[Category.category_id.name].unique()):
            if n:
                category_ids.append(int(n))
        q = (db.session.query(Category.category_id, Category.category_name)
             .filter(Category.category_id.in_(category_ids))
             .order_by(Category.category_id)
             )
        self.category_df = pd.read_sql(q.statement, db.session.bind, index_col=Category.category_id.name)

    def merge_func_category(self):
        """
        :return:
        """
        self.func_df = pd.merge(self.func_df, self.category_df,
                                left_on=Functions.category_id.name,
                                right_index=True,
                                how='left')
        self.func_df[Category.category_name.name].fillna('', inplace=True)

    def get_func_group_df(self):
        return self.func_group_df

    def get_func_group_df2(self):
        func_group_df = self.func_group_df
        group_df = get_group_df()
        func_group_df = pd.merge(func_group_df, group_df,
                                 left_on="group_id",
                                 right_on="group_id",
                                 how="left")
        func_group_df.set_index(["func_id", "group_name"], inplace=True)
        func_group_df = func_group_df.loc[:, [FuncGroup.group_role.name]]
        # print(func_group_df.index)
        # print(func_group_df)
        unstack_df = func_group_df.unstack(level=1)
        unstack_df.columns = unstack_df.columns.droplevel([0])
        # print(unstack_df)
        return unstack_df

    def load_lastest_issus_df(self):
        """
        issue状态：["打开", "已确认", "关闭"]
        :return:
        """
        if self.manday_df is None:
            return
        base_ids = [int(n) for n in list(self.manday_df[FuncManDay.base_id.name].unique())]
        # print(base_ids)
        q = (db.session.query(Issue.key_id, Issue.issue_id, Issue.status)
             .filter(Issue.table_name == FuncManDay.__tablename__)
             .filter(Issue.key_id.in_(base_ids))
             )
        issus_df = pd.read_sql(q.statement, db.session.bind)
        # print(issus_df.columns)
        columns = {Issue.status.name: 'issue_status'}
        # 取最新的指摘
        if issus_df.empty:
            issus_df.set_index(keys=Issue.key_id.name, inplace=True)
            issus_df.rename(columns=columns, inplace=True)
            issus_df.drop([Issue.issue_id.name], axis=1, inplace=True)
            return issus_df
        lastest_issus_df = issus_df.groupby(Issue.key_id.name).apply(top, columns=Issue.issue_id.name, n=1)
        lastest_issus_df.rename(columns=columns, inplace=True)
        # pd.DataFrame().set_index()
        lastest_issus_df.set_index(keys=[Issue.key_id.name], inplace=True)
        # lastest_issus_df.drop([Issue.key_id.name, Issue.issue_id.name], axis=1, inplace=True)
        # print(lastest_issus_df)
        # print(lastest_issus_df.columns)
        return lastest_issus_df

    def load_quotation_option(self):
        q = (db.session.query(OptionCombination.id, OptionCombination.value)
             .filter(OptionCombination.quotation_id == self.quotation_id)
             .order_by(OptionCombination.id)
             )
        self.option_df = pd.read_sql(q.statement, db.session.bind, index_col=OptionCombination.id.name)

    def merge_manday_issus(self, lastest_issus_df):
        """合并工数和指摘状态
        """
        self.manday_df = pd.merge(self.manday_df, lastest_issus_df,
                                  left_on=FuncManDay.base_id.name,
                                  right_index=True,
                                  # right_on=Issue.key_id.name,
                                  how='left')
        self.manday_df['issue_status'].fillna('none', inplace=True)

    # def load_manday_group_df(self):
    #     group_ids = list(self.manday_df.index.levels[0].values)
    #     group_ids = [int(n) for n in group_ids]
    #     q = (db.session.query(Group.group_id, Group.group_name).filter(Group.group_id.in_(group_ids)))
    #     manday_group_df = pd.read_sql(q.statement, db.session.bind)
    #     return manday_group_df

    def summary_manday_by_func(self, option_ids, proj_id):
        """按Function/Feature汇总工数
        :return:
        """
        task_df = self.get_task_df()
        task_df = task_df[[Task.task_id.name, Task.func_id.name]]
        # print(self.manday_df)
        manday_df = self.manday_df
        # print(manday_df)
        culs = (FuncManDay.days.name, Preconditions.precondition.name, FuncManDay.comment.name, FuncStatus.status.name)
        sub_manday_df = manday_df.loc[:, culs]
        # 去掉所有工数内容是空的行
        sub_manday_df = sub_manday_df.replace(0.0, np.NaN)
        sub_manday_df.replace('', np.NaN, inplace=True)
        sub_manday_df = sub_manday_df.dropna(how='all')
        sub_manday_df = sub_manday_df.reset_index(level=[0, 1])
        merged_task_manday_df = pd.merge(task_df, sub_manday_df,
                                         left_on=Task.task_id.name, right_index=True,
                                         how='inner')
        merged_task_manday_df[Preconditions.precondition.name].fillna('', inplace=True)
        merged_task_manday_df[FuncManDay.comment.name].fillna('', inplace=True)
        merged_task_manday_df[FuncStatus.status.name].fillna('处理中', inplace=True)
        group_df = get_group_df()
        gl_sgl_df = get_gl_sgl_df(proj_id)
        gl_sgl_df.drop(['group_name', 'parent_group_id'], axis=1, inplace=True)
        # print(merged_task_manday_df[FuncManDay.group_id.name])
        merged_task_manday_group_df = pd.merge(merged_task_manday_df, group_df,
                                               left_on=FuncManDay.group_id.name,
                                               right_on=Group.group_id.name,
                                               how='inner')
        # print(merged_task_manday_group_df[FuncManDay.group_id.name])
        # print(gl_sgl_df[FuncManDay.group_id.name])
        merged_task_manday_group_df = pd.merge(merged_task_manday_group_df, gl_sgl_df,
                                               left_on=FuncManDay.group_id.name,
                                               right_on=Group.group_id.name,
                                               how='left')
        merged_task_manday_group_df.fillna('', inplace=True)
        # merged_task_manday_group_df[Preconditions.precondition.name] = merged_task_manday_group_df[Preconditions.precondition.name].astype(np.str)
        # merged_task_manday_group_df[Group.group_name.name] = merged_task_manday_group_df[Group.group_name.name].astype(np.str)
        # merged_task_manday_group_df[FuncStatus.status.name] = merged_task_manday_group_df[FuncStatus.status.name].astype(np.str)
        # merged_task_manday_group_df[FuncManDay.comment.name] = merged_task_manday_group_df[FuncManDay.comment.name].astype(np.str)
        # pd.DataFrame().groupby()
        merged_task_manday_group_df[FuncManDay.days.name].replace('', np.NaN, inplace=True)
        # print(merged_task_manday_group_df[FuncManDay.days.name])
        merged_task_manday_group_df[FuncManDay.days.name] = merged_task_manday_group_df[FuncManDay.days.name].astype(np.float)
        # print(merged_task_manday_group_df[FuncManDay.days.name])
        manday_option_df = merged_task_manday_group_df.groupby([FuncManDay.option_id.name])
        manday_option_summary_df = manday_option_df.agg({FuncManDay.days.name: sum})
        # manday_func_df = merged_task_manday_group_df.groupby([Task.func_id.name])
        # manday_func_summary_df = manday_func_df.agg({FuncManDay.days.name: sum})
        # manday_func_summary_df.rename(columns={'days': 'summary_days'}, inplace=True)
        option_summary_dict = manday_option_summary_df.to_dict("index")
        grouped_df = merged_task_manday_group_df.groupby([Task.func_id.name, FuncManDay.option_id.name])
        summary_df = grouped_df.agg({FuncManDay.days.name: sum,
                                     Group.group_name.name: list,
                                     "parent_group_name": list,
                                     Preconditions.precondition.name: list,
                                     FuncStatus.status.name: list,
                                     FuncManDay.comment.name: list})
        func_df = self.get_func_df()
        if not summary_df.empty:
            summary_df = summary_df.unstack(level=1)  # 行转成列
            summary_df = summary_df.swaplevel(i=0, j=1, axis=1)  # 字段和Option换一下
            # print("行转成列===========\n", summary_df)
        func_id_df = func_df[[Functions.func_id.name]]
        func_id_df.set_index(keys=Functions.func_id.name, inplace=True, drop=False)
        # print("func_id_df===============\n", func_id_df)
        func_id_df.columns = pd.MultiIndex.from_tuples([(0, 'func_id'), ], names=['option_id', 'manday'])
        # print("func_id_df===============\n", func_id_df)
        summary_df2 = pd.merge(func_id_df, summary_df,
                               left_index=True, right_index=True,
                               how='left')
        summary_df2.fillna('', inplace=True)
        option_df_dict = {}
        for option_id in option_ids:
            if option_id in summary_df2.columns:
                option_df = summary_df2.loc[:, (option_id, slice(None))]
                option_df.columns = option_df.columns.droplevel([0])  # drop opttion_id, group_id
                option_df_dict[option_id] = option_df
            else:
                option_df_dict[option_id] = None
        return option_df_dict, option_summary_dict

    def summary_manday_by_category(self):
        """按category汇总工数
        :return:
        """
        task_df = self.get_task_df()
        task_df = task_df[[Task.task_id.name, Task.func_id.name]]
        manday_df = self.manday_df.reset_index('task_id')
        merged_task_manday_df = pd.merge(task_df, manday_df,
                                         left_on=Task.task_id.name, right_on=FuncManDay.task_id.name,
                                         how='inner')
        func_df = self.get_func_df()
        merged_task_manday_func_df = pd.merge(func_df, merged_task_manday_df,
                                              left_on=Functions.func_id.name, right_on=Task.func_id.name,
                                              how='left')
        grouped_df = merged_task_manday_func_df.groupby(Category.category_name.name)
        grouped_df[FuncManDay.days.name].fillna(0, inplace=True)
        summary_df = grouped_df.agg({FuncManDay.days.name: sum})
        return summary_df

    def summary_manday_by_sgl(self):
        """按sgl汇总工数
        :return:
        """
        manday_df = self.manday_df.reset_index('group_id')
        group_ids = [int(n) for n in list(manday_df[FuncManDay.group_id.name].unique())]
        q = (db.session.query(Group.parent_group_id)
             .filter(Group.group_id.in_(group_ids))
             )
        parent_group_df = pd.read_sql(q.statement, db.session.bind)
        parent_group_ids = [int(n) for n in list(parent_group_df[Group.parent_group_id.name].unique())]
        q1 = (db.session.query(Group.group_id, Users.user_name)
            .join(Users, Group.owner_user == Users.user_id)
            .filter(Group.group_id.in_(parent_group_ids))
            )
        sgl_group_df = pd.read_sql(q1.statement, db.session.bind)

        q2 = (db.session.query(Group.group_id, Group.group_name, Group.parent_group_id))
        group_df = pd.read_sql(q2.statement, db.session.bind)
        merged_manday_group_df = pd.merge(manday_df, group_df,
                                          left_on=FuncManDay.group_id.name,
                                          right_on=Group.group_id.name,
                                          how='inner')
        merged_manday_sgl_group_df = pd.merge(merged_manday_group_df, sgl_group_df,
                                              left_on=Group.parent_group_id.name,
                                              right_on=Group.group_id.name,
                                              how='inner')
        grouped_df = merged_manday_sgl_group_df.groupby(Users.user_name.name)
        summary_df = grouped_df.agg({FuncManDay.days.name: sum})

        return summary_df

    def summary_manday_by_gl(self):
        """按gl汇总工数
        :return:
        """
        manday_df = self.manday_df.reset_index('group_id')
        group_ids = [int(n) for n in list(manday_df[FuncManDay.group_id.name].unique())]

        q_gl = (db.session.query(Group.group_id, Group.group_name, Users.user_name)
                .join(Users, Group.owner_user == Users.user_id)
                .filter(Group.group_id.in_(group_ids)))
        gl_df = pd.read_sql(q_gl.statement, db.session.bind)
        manday_df[FuncManDay.group_id.name] = manday_df[FuncManDay.group_id.name].astype(np.int)
        gl_df[Group.group_id.name] = gl_df[Group.group_id.name].astype(np.int)
        merged_manday_gl_df = pd.merge(manday_df, gl_df,
                                       left_on=FuncManDay.group_id.name,
                                       right_on=Group.group_id.name,
                                       how='inner')
        grouped_df = merged_manday_gl_df.groupby(Group.group_name.name)
        summary_df = grouped_df.agg({FuncManDay.days.name: sum})

        return summary_df

    def get_func_task_manday(self):
        func_task_df = self.get_func_task_df()
        func_task_df = func_task_df.drop([Task.group_id.name], axis=1)
        task_ids = [int(n) for n in list(func_task_df[Task.task_id.name].unique())]
        q_manday = (db.session.query(FuncManDay)
                    .filter(FuncManDay.task_id.in_(task_ids))
                    .order_by(FuncManDay.update_time.desc()))
        manday_df = pd.read_sql(q_manday.statement, db.session.bind)
        merged_df = pd.merge(func_task_df, manday_df,
                             left_on=Task.task_id.name,
                             right_on=FuncManDay.task_id.name,
                             how='inner')
        return merged_df

    def get_manday_df(self):
        return self.manday_df
