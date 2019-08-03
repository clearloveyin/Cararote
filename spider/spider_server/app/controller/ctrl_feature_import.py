from app.controller.ctrl_base import CtrlBase
from app.controller.ctrl_feature_base import CtrlFeatureBase


class CtrlFeatureImport(CtrlBase):
    def __init__(self):
        CtrlBase.__init__(self)

    def add_top_feature(self, top_feature_list, top_dict):
        """添加顶层的feature"""
        for top in top_feature_list:
            feature_no, feature_name = self.spilt_feature(top)
            feature_dict = {"feature_no": feature_no,
                            "feature_name": feature_name,
                            "feature_type": "Top Items",
                            "parent_feature_id": 0,
                            }
            self.new_feature_dict(feature_dict)
            feature_id = CtrlFeatureBase().add_feature(feature_dict)
            top_dict[top] = feature_id

    def add_sub_feature(self, parent_sub_df, parent_type, sub_type, parent_dict, sub_dict):
        """添加子feature"""
        for i in range(len(parent_sub_df)):
            parent_sub_dict = parent_sub_df.iloc[i].to_dict()
            parent_feature = parent_sub_dict.get(parent_type)
            sub_feature = parent_sub_dict.get(sub_type)
            parent_feature_id = parent_dict.get(parent_feature)
            feature_no, feature_name = self.spilt_feature(sub_feature)
            sub_feature_dict = {"feature_no": feature_no,
                                "feature_name": feature_name,
                                "feature_type": sub_type,
                                "parent_feature_id": parent_feature_id,
                                }
            self.new_feature_dict(sub_feature_dict)
            feature_id = CtrlFeatureBase().add_feature(sub_feature_dict)
            if isinstance(sub_dict, dict):
                sub_dict[sub_feature] = feature_id

    def spilt_feature(self, feature_val):
        split_list = feature_val.split(" ", 1)
        if len(split_list) < 2:
            print(split_list)
        feature_no = split_list[0].strip()
        feature_name = split_list[1].strip()
        return feature_no, feature_name

    def new_feature_dict(self, feature_dict):
        feature_dict['ver'] = self.update_version(ver=0)
        feature_dict["status"] = "发布"
        feature_dict["create_user"] = 1
        feature_dict["create_time"] = self.get_current_time()