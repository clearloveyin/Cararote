from app.db import db
import pandas as pd
from app.controller.ctrl_feature_import import CtrlFeatureImport


class ServiceFeatureImport(object):
    def __init__(self, start_row, col_list, excel_path, sheet_name):
        self.start_row = start_row
        self.col_list = col_list
        self.excel_path = excel_path
        self.sheet_name = sheet_name

    def distinct_feature(self, feature_list):
        news_list = []
        for feature in feature_list:
            if feature not in news_list:
                news_list.append(feature)
        return news_list

    def read_feature_excel(self):
        top_dict = dict()
        middle_dict = dict()
        bottom_dict = dict()
        df = pd.read_excel(self.excel_path,
                           sheetname=self.sheet_name,
                           header=self.start_row,
                           usecols=self.col_list
                           )
        df["Top Items"].fillna(method="ffill", inplace=True)
        df["Middle Items"].fillna(method="ffill", inplace=True)
        df["Bottom Items"].fillna(method="ffill", inplace=True)
        df["Func ID"] = df["F ID"].str.cat(df["Func Name"], sep=" ")  # 合并成一列，用空格分隔
        top_feature_list = self.distinct_feature(df["Top Items"].tolist())
        top_middle_df = df[["Top Items", "Middle Items"]].drop_duplicates()
        middle_bottom_df = df[["Middle Items", "Bottom Items"]].drop_duplicates()
        bottom_func_df = df[["Bottom Items", "Func ID"]].drop_duplicates()
        ctrl_obj = CtrlFeatureImport()
        CtrlFeatureImport.add_top_feature(top_feature_list, top_dict)
        ctrl_obj.add_sub_feature(top_middle_df, parent_type="Top Items", sub_type="Middle Items",
                             parent_dict=top_dict, sub_dict=middle_dict)
        ctrl_obj.add_sub_feature(middle_bottom_df, parent_type="Middle Items", sub_type="Bottom Items",
                             parent_dict=middle_dict, sub_dict=bottom_dict)
        ctrl_obj.add_sub_feature(bottom_func_df, parent_type="Bottom Items", sub_type="Func ID",
                             parent_dict=bottom_dict, sub_dict=None)
        db.session.commit()
