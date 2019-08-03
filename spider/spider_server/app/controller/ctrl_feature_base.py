from app.db import db
from app.controller.ctrl_base import CtrlBase
from app.db.feature_func import Feature


class CtrlFeatureBase(CtrlBase):
    def __init__(self):
        CtrlBase.__init__(self)
        self.sub_feature_list = []

    def get_feature(self, feature_id, ver):
        """根据feature_id和ver获取一条feature"""
        q = (db.session.query(Feature)
             .filter(Feature.feature_id == feature_id)
             .filter(Feature.ver == ver).first())
        return q

    def add_feature(self, feature_dict):
        """添加一条feature"""
        feature_id = self.get_common_key_id(type="Feature")
        feature_dict[Feature.feature_id.name] = feature_id
        new_feature = Feature(**feature_dict)
        db.session.add(new_feature)
        return feature_id

