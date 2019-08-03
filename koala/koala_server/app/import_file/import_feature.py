# -*- coding: UTF-8 -*-
import numpy as np
import pandas as pd
FEATURE_LIST_TEMPLATE = {
    "sheet_name": "Sheet1",
    "header_row": 3,
}


class ImportFeatureList(object):
    """导入报价的技能。"""
    def __init__(self):
        # CtrlBase.__init__(self)
        pass

    def import_excel(self, file_path):
        data_list = self._import_excel(file_path)
        # try:
        #     db.session.query(KnowledgeClassify).delete()
        #     for data in data_list:
        #         db.session.add(KnowledgeClassify(**data))
        #     db.session.commit()
        #     return True, ''
        # except Exception as e:
        #     db.session.rollback()
        #     current_app.logger.error('%s' % e)
        #     return False, "服务异常！请联系管理员！"

    def get_feature_tree(self, file_path):
        feature_tree = self._import_excel(file_path)
        return feature_tree

    def get_feature_tree3(self, file_path):
        feature_tree = self._import_excel3(file_path)
        return feature_tree

    def get_features(self, feature_tree):
        feature_list = []
        for root in feature_tree:
            for one_feature_list in self._get_feature(root):
                feature_list.append(one_feature_list)
        return feature_list

    def _get_feature(self, root):
        """深度搜索
        :param root:
        :return:
        """
        visited = [root]
        sub = root.get("sub")
        if not sub:
            yield [root]
        child_models = list(sub)
        stack = [iter(child_models)]
        while stack:
            children = stack[-1]
            child = next(children, None)
            if child is None:
                stack.pop()
                visited.pop()
            else:
                sub = child.get("sub")
                if not sub:
                    yield visited + [child]
                else:
                    visited.append(child)
                    stack.append(iter(list(sub)))

    def _import_excel(self, file_path):
        df = pd.read_excel(file_path,
                           sheetname=FEATURE_LIST_TEMPLATE.get("sheet_name"),
                           header=FEATURE_LIST_TEMPLATE.get("header_row"),
                           )
        category_idx, featurelist_end_idx, comment_idx, parent_group_idx, group_idx = self.get_category_days_index(df)
        if category_idx >= comment_idx:
            raise Exception("Does not exist [Category]column.")
        if category_idx < 0:
            raise Exception("Does not exist [Category] column.")
        if featurelist_end_idx <= 0:
            raise Exception("Does not exist [Manday/工数] column.")
        if not df.empty and df["Category"].isna()[0]:  # 首行的Category是空
            raise Exception("Category Is NULL.")
        if comment_idx:
            df = df.iloc[:, category_idx:comment_idx+1]
            columns = list(df.columns.values)[category_idx:comment_idx+1]
            comment_df = df.iloc[:, comment_idx:comment_idx + 1]
            comment_df.fillna('', inplace=True)
            df[columns[comment_idx]] = comment_df[columns[comment_idx]]
        else:
            df = df.iloc[:, category_idx:group_idx+1]
            columns = list(df.columns.values)[category_idx:group_idx]
        classify_df = df.iloc[:, category_idx:category_idx + 1]
        classify_df = classify_df.fillna(method='ffill')  # 把空格填上前值
        df[columns[parent_group_idx]].fillna('', inplace=True)
        df[columns[group_idx]].fillna('', inplace=True)
        df[columns[category_idx]] = classify_df[columns[category_idx]]
        start_id = category_idx + 1
        classify_tree = self._get_tree(df, start_id, category_idx, featurelist_end_idx,
                                       comment_idx, columns, parent_group_idx, group_idx)
        return classify_tree

    def _import_excel3(self, file_path):
        df = pd.read_excel(file_path,
                           sheetname=FEATURE_LIST_TEMPLATE.get("sheet_name"),
                           header=FEATURE_LIST_TEMPLATE.get("header_row"),
                           )
        category_idx, featurelist_end_idx, comment_idx = self.get_category_days_index3(df)
        if category_idx >= comment_idx:
            raise Exception("Does not exist [Category]column.")
        if category_idx < 0:
            raise Exception("Does not exist [Category] column.")
        if featurelist_end_idx <= 0:
            raise Exception("Does not exist [Manday/工数] column.")
        if not df.empty and df["Category"].isna()[0]:  # 首行的Category是空
            raise Exception("Category Is NULL.")
        if comment_idx:
            df = df.iloc[:, category_idx:comment_idx+1]
            columns = list(df.columns.values)[category_idx:comment_idx+1]
            comment_df = df.iloc[:, comment_idx:comment_idx + 1]
            comment_df.fillna('', inplace=True)
            df[columns[comment_idx]] = comment_df[columns[comment_idx]]
        else:
            df = df.iloc[:, category_idx:featurelist_end_idx+1]
            columns = list(df.columns.values)[category_idx:featurelist_end_idx]
        classify_df = df.iloc[:, category_idx:category_idx + 1]
        classify_df = classify_df.fillna(method='ffill')  # 把空格填上前值
        # df[columns[parent_group_idx]].fillna('', inplace=True)
        # df[columns[group_idx]].fillna('', inplace=True)
        df[columns[category_idx]] = classify_df[columns[category_idx]]
        start_id = category_idx + 1
        classify_tree = self._get_tree3(df, start_id, category_idx, featurelist_end_idx,
                                        comment_idx, columns)
        return classify_tree

    def get_sub_row(self, parent_row, sub_row, columns):
        for col in columns:
            if parent_row[col] != sub_row[col]:
                if sub_row[col]:
                    break
                sub_row[col] = parent_row[col]
        return sub_row

    def replace_nan(self, row):
        """
        把一行的nan替换成空
        :param row:
        :return:
        """
        for key in row:
            if str(row[key]) == 'nan':
                row[key] = None
        return row

    def deal_with_classify(self, df, curr_col_idx=0):
        classfy_list = pd.unique(df.iloc[:, curr_col_idx])
        print(classfy_list)
        for classfy in classfy_list:
            sub_df = classfy_list[classfy_list[curr_col_idx] == classfy]
            for sub_df in sub_df:
                pass

    def get_category_days_index(self, df):
        """
        :param df: Feature List DataFrame
        :return: category index, comment index, days idx, feature list end index
        """
        col_names = list(df.columns.values)
        parent_group_idx, group_idx, category_idx, comment_idx, days_idx, featurelist_end_idx = -1, -1, -1, -1, -1, 0
        for i, col_name in enumerate(col_names):
            col_name = col_name.strip().lower()
            if col_name.startswith("大组"):
                parent_group_idx = i
            if col_name.startswith("小组"):
                group_idx = i
            if col_name == "category":
                category_idx = i
            if col_name.startswith("工数"):
                days_idx = i
            if col_name.startswith("comment"):
                comment_idx = i
            if not col_name:
                featurelist_end_idx = i
        if comment_idx > 0 and days_idx > 0:
            featurelist_end_idx = min([comment_idx, days_idx]) - 1
        elif comment_idx > 0:
            featurelist_end_idx = min(comment_idx) - 1
        elif days_idx > 0:
            featurelist_end_idx = min(days_idx) - 1
        if featurelist_end_idx <= 0:
            featurelist_end_idx = len(col_names) - 1
        return category_idx, featurelist_end_idx, comment_idx, parent_group_idx, group_idx

    def get_category_days_index3(self, df):
        """
        :param df: Feature List DataFrame
        :return: category index, comment index, days idx, feature list end index
        """
        col_names = list(df.columns.values)
        category_idx, comment_idx, days_idx, featurelist_end_idx = -1, -1, -1, 0
        for i, col_name in enumerate(col_names):
            col_name = col_name.strip().lower()
            if col_name == "category":
                category_idx = i
            if col_name.startswith("工数"):
                days_idx = i
            if col_name.startswith("comment"):
                comment_idx = i
            if not col_name:
                featurelist_end_idx = i
        if comment_idx > 0 and days_idx > 0:
            featurelist_end_idx = min([comment_idx, days_idx]) - 1
        elif comment_idx > 0:
            featurelist_end_idx = min(comment_idx) - 1
        elif days_idx > 0:
            featurelist_end_idx = min(days_idx) - 1
        if featurelist_end_idx <= 0:
            featurelist_end_idx = len(col_names) - 1
        return category_idx, featurelist_end_idx, comment_idx

    def check_column(self, df, columns=None):
        curr_cols = list(df.columns.values)
        error_list = []
        if curr_cols != columns:
            for curr, temp in zip(curr_cols, columns):
                if curr != temp:
                    s = 'title不对，当前[%s], 正确[%s]' % (curr, temp)
                    error_list.append(s)
        return error_list

    def get_knowledge_classify(self, knowledge_only='right', knowledge=''):
        """
        :param knowledge: 知识点类别（线程、等）
        :param knowledge_only: 只取知识点，下面的分级不要。
        :return: Tree(知识点->分级1->分级2...->方档编号)
        """
        # q = db.session.query(FEATURE_LIST_TEMPLATE).order_by(FEATURE_LIST_TEMPLATE.gid)
        # curr_col_idx = 1  # skip: GID
        # if knowledge_only and knowledge_only.lower() in ('left',):
        #     k_df = pd.read_sql(q.statement, db.session.bind)
        #     knowledge_list = list(pd.unique(k_df.iloc[:, curr_col_idx]))
        #     knowledge_tree = {"tag": "技术文档", 'required': True,
        #                       'disabled': True, "sub_tags": [],
        #                       'type': "技术文档"}
        #     if knowledge_list:
        #         knowledge_tree["sub_tags"] = [{"tag": k, 'required': True,
        #                                        'disabled': True,
        #                                        'type': 'knowledge',
        #                                        "sub_tags": []}
        #                                       for k in list(knowledge_list)]
        #     return knowledge_tree
        # else:
        #     if knowledge:
        #         q = q.filter(FEATURE_LIST_TEMPLATE.knowledge == knowledge)
        #     k_df = pd.read_sql(q.statement, db.session.bind)
        #     max_col = len(FEATURE_LIST_TEMPLATE.__table__.columns) - 2
        #     classify_tree = self._get_tree(k_df, curr_col_idx, max_col)
        #     return classify_tree

    def _get_tree(self, df, curr_col_idx, category_idx, featurelist_end_idx,
                  comment_idx, columns, parent_group_idx, group_idx):
        curr_func_df = df.iloc[:, curr_col_idx:curr_col_idx+1]
        curr_func_df = curr_func_df.fillna(method='ffill')
        df[columns[curr_col_idx]] = curr_func_df[columns[curr_col_idx]]
        func_list = pd.unique(curr_func_df.iloc[:, 0])
        sub_list = []
        for func in func_list:
            # print(func)
            column = columns[curr_col_idx]
            sub_df = df[df[column] == func]
            comment = ''
            if comment_idx > 0:
                comment = sub_df.iat[0, comment_idx]
            parent_group = sub_df.iat[0, parent_group_idx]
            group = sub_df.iat[0, group_idx]
            category = sub_df.iat[0, category_idx]
            func_dict = {"name": func, "sub": [], "category": category,
                         "comment": str(comment), "parent_group": parent_group, "group": group}
            if curr_col_idx == featurelist_end_idx:
                pass
            else:
                next_column = columns[curr_col_idx + 1]
                sub_df = sub_df.dropna(subset=[next_column])
                sub = self._get_tree(sub_df, curr_col_idx + 1, category_idx, featurelist_end_idx,
                                     comment_idx, columns, parent_group_idx, group_idx)
                func_dict["sub"] = sub
            sub_list.append(func_dict)
        return sub_list

    def _get_tree3(self, df, curr_col_idx, category_idx, featurelist_end_idx,
                   comment_idx, columns):
        curr_func_df = df.iloc[:, curr_col_idx:curr_col_idx+1]
        curr_func_df = curr_func_df.fillna(method='ffill')
        curr_func_df.fillna('', inplace=True)
        df[columns[curr_col_idx]] = curr_func_df[columns[curr_col_idx]]
        func_list = pd.unique(curr_func_df.iloc[:, 0])
        sub_list = []
        for func in func_list:
            # print(func)
            column = columns[curr_col_idx]
            sub_df = df[df[column] == func]
            comment = ''
            if comment_idx > 0:
                comment = sub_df.iat[0, comment_idx]
            category = sub_df.iat[0, category_idx]
            func_dict = {"name": str(func), "sub": [], "category": category,
                         "comment": str(comment)}
            if curr_col_idx == featurelist_end_idx:
                pass
            else:
                next_column = columns[curr_col_idx + 1]
                # sub_df = sub_df.dropna(subset=[next_column])
                sub = self._get_tree3(sub_df, curr_col_idx + 1, category_idx, featurelist_end_idx,
                                      comment_idx, columns)
                func_dict["sub"] = sub
            sub_list.append(func_dict)
        return sub_list

    def _get_doc_ids(self, df, curr_col_idx, max_col):
        """当前分类下的文档
        :param df:
        :param curr_col_idx:
        :return:
        """
        if curr_col_idx == max_col:
            doc_id_list = list(pd.unique(df.iloc[:, -1]))
        else:
            next_column = FEATURE_LIST_TEMPLATE.get("re_column")[curr_col_idx]
            # print(next_column)
            na_df = df[df[next_column].isnull()]  # 空：是叶子
            # print(na_df)
            doc_id_list = list(pd.unique(na_df.iloc[:, -1]))
        doc_id_list = [int(n) for n in doc_id_list]
        return doc_id_list


if __name__ == '__main__':
    obj = ImportFeatureList()
    file_path = r'C:\Users\hongchenzai\Desktop\21mm_FeatureList_template_ver0.2_huang.xlsx'
    import datetime
    print(datetime.datetime.now())
    feature_tree = obj.get_feature_tree3(file_path)
    feature_list = obj.get_features(feature_tree)
    print(len(feature_list))
    print(datetime.datetime.now())
    # feature_tree = obj.get_feature_tree(file_path)
    # feature_list = obj.get_features(feature_tree)
    # print(feature_tree)

