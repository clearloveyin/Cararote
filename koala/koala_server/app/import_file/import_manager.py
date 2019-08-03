# -*- coding: UTF-8 -*-
import pandas as pd

MANAGER_TEMPLATE = {
    "sheet_name": "manager",
    "header_row": 13,
}


class ImportManager(object):
    """导入报价的技能。"""
    def __init__(self):
        # CtrlBase.__init__(self)
        pass

    def import_excel(self, file_path):
        try:
            return True, self._import_excel(file_path)
        except Exception as e:
            return False, '%s%s' % (str(e), "文件解析失败，请检查文件是否正确")

    def _import_excel(self, file_path):
        df = pd.read_excel(file_path,
                           sheet_name=MANAGER_TEMPLATE.get("sheet_name"),
                           header=MANAGER_TEMPLATE.get("header_row"),
                           # skiprows=MANAGER_TEMPLATE.get("header_row") + 1
                           usecols=[2, 3, 4, 5]  # 使用第2列到第5列
                           )
        df.dropna(how='all', inplace=True)
        group_s = df["Group"]
        df["Group"] = group_s.fillna(method='ffill')  # 把空格填上前值
        leader_s = df["Leader"]
        df["Leader"] = leader_s.fillna(method='ffill')  # 把空格填上前值
        df.fillna('', inplace=True)
        # print(df)
        # print(df.to_dict(orient='records'))
        return df


if __name__ == '__main__':
    obj = ImportManager()
    file_path = r'C:\workspace\koala\Spec2DB\koala\koala_server\template\开发体制_template_ver0.1.xlsx'
    # obj._import_excel(file_path)
    feature_tree = obj.import_excel(file_path)
    print(feature_tree)

