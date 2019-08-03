# -*- coding: UTF-8 -*-
import datetime
import json
import pandas as pd
import numpy as np
import platform
import datetime
import copy
from collections import Iterable
from flask import current_app
from app.db import db
from app.db.journal import Journal, JournalBrief, JournalDetail
from sqlalchemy_utils.functions import get_primary_keys


JOURNALIZED_TYPE_BACKUP = 'BACKUP'
JOURNALIZED_TYPE_JOURNAL = 'JOURNAL'


class CtrlJournal(object):
    def __init__(self):
        pass

    def write(self, db_objs, **kwargs):
        """
        :param db_objs: declarative_base(db.Model) object.
        :param journalized_id: (optional)
        :param username: (optional).
        :param journalized_type: (optional).
        :param notes: (Optional).
        :param update_time: (Optional).
        :return: success return True.
        """
        # journalized_id = kwargs.get("journalized_id")
        # if not journalized_id:
        #     current_app.logger.warning('Dose not indicate journalized id[%s].'
        #                                % journalized_id)
        username = kwargs.get("username")
        journalized_type = kwargs.get("journalized_type")
        if not journalized_type:
            journalized_type = JOURNALIZED_TYPE_BACKUP
        notes = kwargs.get("notes")
        create_time = kwargs.get("update_time")
        if not create_time:
            create_time = kwargs.get("create_time")
        journalized_id = self.write_journal(journalized_type, username,
                                            notes, create_time)
        if not journalized_id:
            current_app.logger.error('Write journal failed.')
            return False
        if isinstance(db_objs, Iterable):
            for db_obj in db_objs:
                journal_brief_id = self._write_journal_brief(db_obj,
                                                             journalized_id)
                if not self._write_journal_detail(db_obj,
                                                  journal_brief_id):
                    return False
        else:
            journal_brief_id = self._write_journal_brief(db_objs,
                                                         journalized_id)
            if not journal_brief_id:
                return False
            if not self._write_journal_detail(db_objs, journal_brief_id):
                return False
        return True

    def write_journal(self, journalized_type, username, notes, create_time):
        if not username:
            current_app.logger.error('Dose not indicate user')
            return 0
        from app.ctrl.ctrl_user import CtrlUser
        if not username:
            current_app.logger.error("Dose not indicate user.")
            return 0
        user = CtrlUser().get_user_by_name(username)
        if not user:
            current_app.logger.error("Dose not exist user[%s]." % username)
            return 0
        if not create_time:
            create_time = datetime.datetime.now()
            pass
        journal_info = {Journal.journalized_type.name: journalized_type,
                        Journal.user_id.name: user.user_id,
                        Journal.notes.name: notes,
                        Journal.create_time.name: create_time,
                        }
        journal = Journal(**journal_info)
        db.session.add(journal)
        db.session.flush()
        return journal.journalized_id

    def _write_journal_brief(self, db_obj, journalized_id):
        if not journalized_id:
            return 0
        if db_obj and isinstance(db_obj, db.Model):
            table_name = db_obj.__tablename__
            data = {JournalBrief.table_name.name: table_name,
                    JournalBrief.journalized_id.name: journalized_id,
                    JournalBrief.key_id.name: self.get_key_id(db_obj),
                    JournalBrief.action.name: 'backup',
                    }
            journal_brief = JournalBrief(**data)
            db.session.add(journal_brief)
            db.session.flush()
            return journal_brief.j_brief_id
        else:
            current_app.logger.error("Type is not db.Model. current type[%s]."
                                     % type(db_obj))
            return 0

    def _write_journal_detail(self, db_obj, journal_brief_id):
        if not journal_brief_id:
            return False
        if db_obj and isinstance(db_obj, db.Model):
            # table_name = db_obj.__tablename__
            detail = {JournalDetail.j_brief_id.name: journal_brief_id,
                      # JournalDetail.table_name.name: table_name,
                      # JournalDetail.key_id.name: self.get_key_id(db_obj)
                      }
            for column in db_obj.__table__.columns:
                val = getattr(db_obj, column.name)
                detail[JournalDetail.column_name.name] = column.name
                detail[JournalDetail.val.name] = val
                db.session.add(JournalDetail(**detail))
            return True
        else:
            current_app.logger.error("Type is not db.Model. current type[%s]."
                                     % type(db_obj))
            return False

    def get_key_id(self, db_obj):
        # primary_keys = inspect(db_obj).primary_key
        # primary_keys = get_primary_keys(db_obj)
        # print(db_obj)
        primary_keys = list(get_primary_keys(db_obj).keys())
        if primary_keys:
            key_name = primary_keys[0]
            return getattr(db_obj, key_name)
        else:
            column = db_obj.__table__.columns[0]
            return getattr(db_obj, column.name)

    def get_journal_detail(self, journalized_id):
        sqlcmd = """
        SELECT key_id, table_name, column_name, val
          FROM public.journals as a
          left join public.journal_briefs as b
          on a.journalized_id = b.journalized_id
          left join public.journal_details as c
          on b.j_brief_id = c.j_brief_id
          where a.journalized_id = {journalized_id}
          order by b.j_brief_id, c.j_detail_id
        """.format(journalized_id=journalized_id)
        df = pd.read_sql(sqlcmd, db.session.bind)
        return df

    def get_detatils_by_journalized_id(self, journalized_id):
        q = (db.session.query(JournalDetail)
             .filter(JournalDetail.journalized_id == journalized_id)
             .order_by(JournalDetail.journal_id)
             )
        sqlcmd = q.statement
        df = pd.read_sql(sqlcmd, db.session.bind)
        return df

    def add_journals(self, log, journalized_type=JOURNALIZED_TYPE_JOURNAL):
        journalized_id = self._add_journal(log, journalized_type)
        if not journalized_id:
            return False
        for commit in log.get('commit_list'):
            table_name = commit.get("table_name")
            action = commit.get("action")
            key_id = commit.get("key_id")
            journal_brief_id = self._add_journal_brief(journalized_id, key_id,
                                                       table_name, action)
            data = commit.get("data")
            self._add_journal_detial(journal_brief_id, key_id, data)
        return True

    def _add_journal(self, log, journalized_type):
        # from app.ctrl.ctrl_user import CtrlUser
        user_id = log.get("commit_user")
        if not user_id:
            current_app.logger.error("Dose not indicate user.")
            return 0
        # user = CtrlUser().get_user_by_name(user_name)
        # if not user:
        #     current_app.logger.error("Dose not exist user[%s]." % user_name)
        #     return 0
        # user_id = user.user_id
        data = {Journal.journalized_type.name: journalized_type,
                Journal.create_time.name: log.get("update_time"),
                Journal.user_id.name: user_id,
                }
        journal = Journal(**data)
        db.session.add(journal)
        db.session.flush()
        return journal.journalized_id

    def _add_journal_brief(self, journalized_id, key_id, table_name, action):
        data = {JournalBrief.journalized_id.name: journalized_id,
                JournalBrief.key_id.name: key_id,
                JournalBrief.action.name: action,
                JournalBrief.table_name.name: table_name,
                }
        journal_brief = JournalBrief(**data)
        db.session.add(journal_brief)
        db.session.flush()
        return journal_brief.j_brief_id

    def _add_journal_detial(self, journal_brief_id, key_id, log_data):
        for col in log_data:
            data = {JournalDetail.j_brief_id.name: journal_brief_id,
                    # JournalDetail.key_id.name: key_id,
                    JournalDetail.column_name.name: col,
                    JournalDetail.val.name: log_data[col],
                    }
            journal_detail = JournalDetail(**data)
            db.session.add(journal_detail)


################################################################################
#
################################################################################
class CtrlDSDocJournal(CtrlJournal):
    """基本设计和详细设计
    """
    def __init__(self):
        CtrlJournal.__init__(self)
        self.table_name = 'ds_doc'
        # self.db = Ds_Doc
        self.sub_template = {"doc_id": 0, "sec_type": "", "sub": []}
        self.df_keys = [JournalBrief.key_id.name,
                        JournalBrief.table_name.name,
                        JournalDetail.column_name.name]
        self.failure_df = None
        self.scene_df = None
        self.model_df = None
        self.failure_model_df = None

    # def get_journal_diff(self, key_id, left_version=0, right_version=0):
    #     """
    #     :param key_id: 如doc_id
    #     :param log_type: 类别
    #     :param left_version: 左边版本号(Old)
    #     :param right_version: 右边版本号(New)
    #     :return:
    #     """
    #     from app.ctrl.ctrl_ds_doc import CtrlDsDoc
    #     # try:
    #     if not right_version or right_version == '0':  # 0: 最新。空：未指定
    #         db_objs = CtrlDsDoc().get_db_for_journal2(key_id)
    #         right_df = self._db_objs_2_df(db_objs)
    #         right_version = 0
    #     else:
    #         right_version = int(right_version)
    #         right_df = self.get_journal_detail(right_version)
    #     if left_version == '0':
    #         db_objs = CtrlDsDoc().get_db_for_journal2(key_id)
    #         left_df = self._db_objs_2_df(db_objs)
    #     elif not left_version:  # 空：未指定，使用日志里，最近的一条。
    #         left_journalized_id = self._get_journalized_id(key_id, '')
    #         if left_journalized_id:
    #             left_df = self.get_journal_detail(left_journalized_id)
    #             left_version = left_journalized_id
    #         else:
    #             left_df = pd.DataFrame()
    #     elif left_version:
    #         left_version = int(left_version)
    #         left_df = self.get_journal_detail(left_version)
    #     else:
    #         left_df = pd.DataFrame()
    #     if not left_df.empty:
    #         left_doc = self.df_2_doc(left_df, right_df, 'left')
    #         left_doc["version"] = left_version
    #         # print(right_df)
    #         right_doc = self.df_2_doc(right_df, left_df, 'right')
    #         right_doc["version"] = right_version
    #         return left_doc, right_doc, "OK"
    #     right_doc = self.df_2_doc(right_df, None, 'right')
    #     right_doc["version"] = right_version
    #     return dict(), right_doc, "OK"
    #     # except Exception as e:
    #     #     return dict(), dict(), str(e)

    def _db_objs_2_df(self, db_objs):
        columns = [JournalBrief.key_id.name, JournalBrief.table_name.name,
                   JournalDetail.column_name.name, JournalDetail.val.name]
        data = []
        for db_obj in db_objs:
            data += self._db_obj_2_records(db_obj)
        df = pd.DataFrame(data=data, columns=columns)
        return df

    def _db_obj_2_records(self, db_obj):
        records = []
        key_id = self.get_key_id(db_obj)
        table_name = db_obj.__tablename__
        # print(table_name)
        for column in db_obj.__table__.columns:
            val = getattr(db_obj, column.name)
            # if(isinstance(val, datetime.datetime)
            #    or isinstance(val, datetime.time)):
            if val is None:
                val = ''
            else:
                val = str(val)
            records.append((key_id, table_name, column.name, val))
        return records

    def get_journalized_versions(self, key_id):
        journalized_id_list = []
        rows = self._get_journalized_infos(key_id)
        for row in rows:
            journalized_id_list.append(row[0])
        journalized_id_list.sort()
        journalized_id_list.append(0)  # 0, 表示当前最新的版本
        return journalized_id_list

    def _get_journalized_id(self, key_id, version):
        """
        :param key_id: doc_id
        :param version: 版本号, 不指定时，返回最近的日志id
        :return: 日志id
        """
        if version:
            major_mino_ver = version.split('.')
        else:
            major_mino_ver = []
        rows = self._get_journalized_infos(key_id)
        for row in rows:
            journalized_id = row[0]
            vers = row[2]
            if major_mino_ver:
                if major_mino_ver == vers:
                    return journalized_id
            else:
                return journalized_id
        return None


    def df_2_doc(self, df1, df2, lf):
        """DataFrame 转成 文档结构(树型结构)
        :param df1:
        :param df2:
        :param lf: left, right
        :return: 文档
        """
        doc_info = self._get_doc_info(df1, df2, lf)
        # TODO@hcz: 比较Doc_id，判断是不是同个文件
        # doc_info["sub"] = []
        doc_id = doc_info.get("doc_id")
        # ## ASTAH
        # astah_info = copy.deepcopy(self.sub_template)
        # astah_info["sec_type"] = "ASTAH"
        # astah_info["doc_id"] = doc_id
        # astah_info["astah_files"] = self._get_astah(df1, df2, lf)
        # doc_info["sub"].append(astah_info)
        # # ## IF接口
        # if_list = self._get_if(df1, df2, lf)
        # doc_info["sub"] = doc_info["sub"] + if_list
        # ## UseCase/Common/Block/Sequence
        sections = self._get_sections(df1, df2, lf, doc_id)
        doc_info.update(sections)
        return doc_info

    def _get_doc_info(self, df, df2, lf):
        doc_df = df[df["table_name"] == 'ds_doc']
        ds_info = self.df_to_dict(doc_df, df2, lf)
        return ds_info

    def _get_astah(self, df, df2, lf):
        attach_list = []
        attach_dfs = self._get_sub_df_list(df, 'ds_attach')
        for attach_df in attach_dfs:
            attach_info = self.df_to_dict(attach_df, df2, lf)
            attach_list.append(attach_info)
        return attach_list

    def _get_if(self, df, df2, lf):
        if_list = []
        if_dfs = self._get_sub_df_list(df, 'ds_doc_if')
        for if_df in if_dfs:
            in_info = self.df_to_dict(if_df, df2, lf)
            in_info["sub"] = []
            in_info["sec_type"] = 'IF'
            if_list.append(in_info)
        return if_list

    def _get_sections(self, df, df2, lf, doc_id):
        """
        :param sec_type: BLOCK/COMMON/USERCASE
        :return:
        """
        sections = {"BLOCK": [], "CLASS": [], "COMMON": [], "USERCASE": [], "STD": []}
        section_df = df[df.table_name == 'ds_section']
        # ## 父
        condition = "column_name == 'parent_sec_id' and val == '0'"
        root_sec_id_df = section_df.query(condition)
        # print(root_sec_id_df)
        sec_ids = list(root_sec_id_df["key_id"].unique())
        sec_journal = CtrlSectionJournal()
        uc_df_list, seq_df_list = [], []
        for sec_id in sec_ids:
            current_sec_df = self._get_current_df(df, sec_id, 'ds_section')
            current_sec = dict()
            current_sec.update(sec_journal.df_to_dict(current_sec_df, df2, lf))
            # current_sec["doc_id"] = doc_id
            if current_sec.get("sec_type") == "USERCASE":
                # 机能点
                uc_df_list.append(current_sec_df)
                # ## 式样书
                # spec = copy.deepcopy(self.sub_template)
                # spec["sec_type"] = "SPEC"
                # spec["specs"] = self._get_specification(df, df2, lf,
                #                                         doc_id, sec_id)
                # current_sec["sub"].append(spec)
                continue
            ## Sequence
            if current_sec.get("sec_type") == "SEQUENCE":
                seq_df_list.append(current_sec_df)
                # 资源
                resource_list = self._get_resource(df, df2, lf, sec_id)
                current_sec["resource"] = resource_list
                # Activity
                activity_list = self._get_sub_section(df, df2, lf, sec_id,
                                                      sec_type='Activity')
                current_sec["activities"] = activity_list
                continue
            sections[current_sec.get("sec_type")].append(current_sec)
        # ## Table listx
        table_list = self._get_table_list(df, df2, lf, uc_df_list, seq_df_list)
        # sections.append({"sec_type": "USERCASE",
        #                  "table_list": table_list,
        #                  "sub": []})
        # # ## DRBFM
        # drbfm_list = self._get_drbfm_new(df, df2, lf, doc_id)
        # if drbfm_list:
        #     drbfm = copy.deepcopy(self.sub_template)
        #     drbfm["doc_id"] = doc_id
        #     drbfm["sec_type"] = "DRBFM"
        #     drbfm["checklist"] = drbfm_list
        #     sections.append(drbfm)
        return sections



    def _cmp_seq_for_table_list(self, merged_df1, merged_df2, uc_number, lf):
        seq_list = []
        sec_journal = CtrlSectionJournal()
        merged_df1 = merged_df1[merged_df1["uc_number"] == uc_number]
        merged_df2 = merged_df2[merged_df2["uc_number"] == uc_number]
        # print('merged_df1\n', merged_df1)
        # print('merged_df2\n', merged_df2)
        # 按Seq的编号
        seq_merge_df = pd.merge(merged_df1, merged_df2, how='left',
                                on='number', suffixes=['', '_b'])
        seq_merge_df.dropna(subset=["sec_id"], inplace=True)
        seq_merge_df.fillna('', inplace=True)
        seq_merge_df.sort_values(["number"], inplace=True)
        for _, row in seq_merge_df.iterrows():
            seq = sec_journal.cmp_content(row["content"], row["content_b"])
            seq.update(row[["sec_id", "sec_type", "number"]].to_dict())
            if not row["sec_id_b"]:
                seq["number"] = self._diff_and_set_color(row["number"], '', lf)
            seq_list.append(seq)
        return seq_list

    def _get_code_df(self, sec_df, sec_type="SEQUENCE"):
        data = []
        for i, row in sec_df.iterrows():
            if sec_type == "USERCASE":
                data.append([row["sec_id"],
                             row["sec_type"],
                             'UC%r' % (i + 1),
                             row["content"]]
                            )
            elif sec_type == "SEQUENCE":
                data.append([row["sec_id"],
                             row["sec_type"],
                             'Sequence%r' % (i + 1),
                             row["content"]]
                            )
        columns = ["sec_id", "sec_type", "number", "content"]
        df = pd.DataFrame(data=data, columns=columns)
        return df

    def _get_current_df(self, df, key_id, table_name):
        condition = 'key_id == @key_id and table_name == @table_name'
        current_sec_df = df.query(condition)
        return current_sec_df

    def _get_sub_df_list(self, df, table_name, cols=None, vals=None):
        if df is None:
            return []
        sub_list = []
        same_table_df = df[df["table_name"] == table_name]
        # print(same_table_df)
        all_ids = list(same_table_df["key_id"].unique())
        sub_ids = set(all_ids)
        if not cols:
            cols = []
        if not vals:
            vals = []
        # ## 求交集
        for col, val in zip(cols, vals):
            condition = "column_name == @col and val == @val"
            temp_df = same_table_df.query(condition)
            temp_ids = list(temp_df["key_id"])
            sub_ids = sub_ids.intersection(temp_ids)
        for key_id in all_ids:
            if key_id not in sub_ids:
                continue
            sub_df = same_table_df[same_table_df["key_id"] == key_id]
            sub_list.append(sub_df)
        return sub_list

    def _set_color(self, d, action, lf):
        v2 = ''
        if action == 'delete':
            for k, v in d.items():
                if k in ("title", ):
                    continue
                if k.endswith('_id') or k.endswith('gid'):
                    continue
                d[k] = self._diff_and_set_color(v, v2, lf)
        elif action == 'add':
            for k, v in d.items():
                if k in ("title", ):
                    continue
                if k.endswith('_id') or k.endswith('gid'):
                    continue
                d[k] = self._diff_and_set_color(v, v2, lf)
        else:
            pass
        return d

    def _get_scenes(self, df, df2, lf, sec_id):
        """
        :param df:
        :param sec_id:
        :return: 场景
        """
        rel_scene_list = []
        table_name = 'ds_rel_scene'
        cols = ['sec_id']
        vals = [str(sec_id)]
        rel_scene_df_list = self._get_sub_df_list(df, table_name, cols, vals)
        if rel_scene_df_list:
            from app.ctrl.ctrl_ds_scene import CtrlDSScene
            scene_dict = CtrlDSScene().get_scene2()
        for rel_spec_df in rel_scene_df_list:
            rel_spec_dict = self.df_to_dict(rel_spec_df, df2, lf)
            scene_id = rel_spec_dict.get("scene_id")
            if scene_id:
                scene_id = int(scene_id)
                scene_info = scene_dict.get(scene_id)
                if scene_info:
                    rel_spec_dict.update(scene_info)
                else:
                    current_app.logger.error('Unknown scene ID [%s].'
                                             % scene_id)
            rel_scene_list.append(rel_spec_dict)
        return rel_scene_list

    def _get_sub_section(self, df, df2, lf, parent_sec_id, sec_type='SEQUENCE'):
        """
        :param df:
        :param sec_id: Usecase section id.
        :return: section
        """
        sequence_list = []
        table_name = 'ds_section'
        cols = ['parent_sec_id', 'sec_type']
        vals = [str(parent_sec_id), sec_type]
        sequence_df_list = self._get_sub_df_list(df, table_name, cols, vals)
        sec_journal = CtrlSectionJournal()
        for sequence_df in sequence_df_list:
            sequence_dict = sec_journal.df_to_dict(sequence_df, df2, lf)
            if sequence_dict.get("sec_type") == "SEQUENCE":
                sec_id = sequence_dict.get("sec_id")
                # Activity
                activity_list = self._get_sub_section(df, df2, lf, sec_id,
                                                      sec_type='Activity')
                sequence_dict["activities"] = activity_list
                # 资源
                resource_list = self._get_resource(df, df2, lf, sec_id)
                sequence_dict["sub"] = resource_list
            sequence_list.append(sequence_dict)
        return sequence_list

    def _get_resource(self, df, df2, lf, sec_id):
        """
        :param df:
        :param sec_id: Sequence section id.
        :return: Resource
        """
        resource_list = []
        table_name = 'ds_section_resource_rel'
        cols = ['sec_id']
        vals = [str(sec_id)]
        resource_info = dict()
        rel_scene_df_list = self._get_sub_df_list(df, table_name, cols, vals)
        if rel_scene_df_list:
            from app.ctrl.ctrl_ds_section import CtrlDSResource
            resource_info_list = CtrlDSResource().get_resource()
            for r in resource_info_list:
                resource_info[r.get("resource_id")] = r
        for resource_df in rel_scene_df_list:
            resource_dict = self.df_to_dict(resource_df, df2, lf)
            resource_dict["sec_type"] = "RESOURCE"
            resource_id = int(resource_dict.get("resource_id"))
            resource = resource_info.get(resource_id)
            if resource:
                resource_dict.update(resource)
            else:
                current_app.logger.error('Unknown Resource ID [%s].'
                                         % resource_id)
            resource_list.append(resource_dict)
        return resource_list

    def _get_consider(self, df, df2, lf, sec_id):
        """
        :param df:
        :param df2:
        :param sec_id: UseCase id.
        :return: consider
        """

        table_name = 'ds_doc_consider'
        cols = ['sec_id']
        vals = [str(sec_id)]
        consider_list = []
        consider_df_list = self._get_sub_df_list(df, table_name, cols, vals)
        for consider_df in consider_df_list:
            consider_dict = self.df_to_dict(consider_df, df2, lf)
            consider_id = int(consider_dict.get("consider_id"))
            consider = self._get_consider_info(consider_id)
            if consider:
                consider_dict.update(consider)
            else:
                current_app.logger.error('Unknown Resource ID [%s].'
                                         % consider_id)
            consider_list.append(consider_dict)
        return consider_list

    def _get_drbfm(self, df, df2, lf, doc_id):
        """
        :param df:
        :param sec_id: Sequence section id.
        :return: DRBFM
        """
        # print('DRBFM Start===: ', datetime.datetime.now())
        drbfm_list = []
        table_name = 'ds_rel_tag'
        cols = ['doc_id']
        vals = [str(doc_id)]
        drbfm_df_list = self._get_sub_df_list(df, table_name, cols, vals)
        if not drbfm_df_list:
            return drbfm_list
        drbfm_cat_df = self._get_drbfm_df(drbfm_df_list, doc_id)
        failure_df = self._get_failure_df()  # 获取着眼点
        scene_df = self._get_scene_df()  # 获取着眼点
        # ##
        drbfm_df_list2 = self._get_sub_df_list(df2, table_name, cols, vals)
        drbfm_cat_df2 = self._get_drbfm_df(drbfm_df_list2, doc_id)
        drbfm_df = pd.merge(failure_df, drbfm_cat_df, on=["item_id"])
        drbfm_df = pd.merge(drbfm_df, scene_df, on=["scene_id"])
        category_list = list(drbfm_df["category"].unique())
        for category in category_list:
            cat_node = {"name": category, "sub": []}
            cat_df = drbfm_df[drbfm_df["category"] == category]
            major_names = list(cat_df["major_item"].unique())
            # 大分类
            for major_item in major_names:
                major_node = {"name": major_item, "sub": []}
                major_df = cat_df[cat_df["major_item"] == major_item]
                failure_names = list(major_df["failure"].unique())
                for failure in failure_names:  # 着眼点
                    fail_item_df = major_df[major_df["failure"] == failure]
                    item_id = fail_item_df.iloc[0]["item_id"]
                    # if platform.system() == 'Windows':
                    #     item_id = int(fail_item_df.iloc[0]["item_id"].astype(np.int))
                    # else:
                    #     item_id = fail_item_df.iloc[0]["item_id"]
                    scene_list = self._get_failure_scenes(fail_item_df,
                                                          drbfm_cat_df2,
                                                          lf)
                    failure_node = {"name": failure,
                                    "item_id": item_id,
                                    "sub": [],
                                    "scenes": scene_list
                                    }
                    major_node["sub"].append(failure_node)
                cat_node["sub"].append(major_node)
            drbfm_list.append(cat_node)
        return drbfm_list

    def _convert_change_content(self, df, change_type, lf):
        change_content = u""
        s = df.iloc[0]
        if change_type == "change":  # 修改点
            before_change = s["before_change"]
            change = s["change"]
            change_content += '修改前:\n'
            if before_change == '同上' and change == '同上':
                return ''
            if not before_change:
                before_change = ''
            before_change_b = s["before_change_b"]
            val = self._diff_and_set_color(before_change, before_change_b, lf)
            change_content += val + '\n'
            change_content += '\n修改后:\n'
            if not change:
                change = ''
            change_b = s["change_b"]
            val = self._diff_and_set_color(change, change_b, lf)
            change_content += val
        else:
            change_content += '影响前:\n'
            before_change = s["before_influence"]
            change = s["influence"]
            if before_change == '同上' and change == '同上':
                return ''
            if not before_change:
                before_change = ''
            cmp_change = s["before_influence_b"]
            val = self._diff_and_set_color(before_change, cmp_change, lf)
            change_content += val + '\n'
            change_content += '\n影响后:\n'
            if not change:
                change = ''
            cmp_change = s["influence_b"]
            val = self._diff_and_set_color(change, cmp_change, lf)
            change_content += val
        return change_content

    def _convert_models(self, df, lf):
        df = df.dropna(subset=["model_id"])
        df = df[["model_id", "model_name", "failure_mode_name",
                 "model_name_b"]]
        model_list = []
        failuremode_num = 0
        model_ids = df["model_id"].unique()
        for model_id in model_ids:
            model_dict = dict()
            model_df = df[df["model_id"] == model_id]
            s = model_df.iloc[0]
            model_name = s["model_name"]
            model_name_b = s["model_name_b"]
            model_dict["model_name"] = self._diff_and_set_color(model_name,
                                                                model_name_b,
                                                                lf)
            model_df = model_df.drop_duplicates()
            failuremode_list = []
            for _, row in model_df.iterrows():
                failure_mode = row["failure_mode_name"]
                if model_name_b:  # 没有变化
                    val = failure_mode
                else:  # 新增
                    val = self._diff_and_set_color(failure_mode, '', lf)
                failuremode_list.append(val)
            if failuremode_list:
                model_dict["failuremode_list"] = failuremode_list
                model_list.append(model_dict)
            failuremode_num += len(failuremode_list)
        return model_list, failuremode_num

    def _get_rel_models(self, df, change_df):
        rel_model_df_list = []
        table_name = 'ds_rel_model'
        cols = ['change_id']
        for _, row in change_df.iterrows():
            change_id = row["change_id"]
            vals = [str(change_id)]
            rel_model_dfs = self._get_sub_df_list(df, table_name, cols, vals)
            rel_model_df_list += rel_model_dfs
        return rel_model_df_list

    def _get_failure_scenes(self, fail_item_df, df2, lf):
        scene_list = []
        merge_df = pd.merge(fail_item_df, df2, how='left',
                            on=["item_id", "scene_id"], suffixes=['', '_b'])
        merge_df = merge_df[["scene_id", "scene",
                             "drbfm_content", "drbfm_content_b"]]
        merge_df["drbfm_content_b"].fillna(value='', inplace=True)
        # print(merge_df)
        for secene_info in merge_df.to_dict(orient='records'):
            v1 = secene_info.pop("drbfm_content", '')
            v2 = secene_info.pop("drbfm_content_b", '')
            new_val = self._diff_and_set_color(v1, v2, lf)
            secene_info["content"] = new_val
            scene_list.append(secene_info)
        return scene_list

    def _get_drbfm_df(self, drbfm_df_list, sec_id):
        df_cat = pd.DataFrame(columns=["sec_id", "item_id",
                                       "scene_id", "drbfm_content"])
        for df in drbfm_df_list:
            drbfm_dict = self.df_to_dict(df, None, lf='left')
            if not drbfm_dict.get("drbfm_content"):
                continue
            drbfm_dict["item_id"] = int(drbfm_dict["item_id"])
            drbfm_dict["scene_id"] = int(drbfm_dict["scene_id"])
            drbfm_dict.pop("gid")
            df_cat = df_cat.append(drbfm_dict, ignore_index=True)
        df_bak = pd.DataFrame(data=df_cat, copy=True)
        scene_id_list = list(df_bak["scene_id"].unique())
        all_items = set(df_bak["item_id"].unique())
        for scene_id in scene_id_list:
            curr_df = df_bak[df_bak["scene_id"] == scene_id]
            curr_items = set(curr_df["item_id"].unique())
            for item_id in all_items.difference(curr_items):
                df_cat.loc[len(df_cat)] = [sec_id, item_id, scene_id, '']
        df_cat.sort_values(by=["item_id", "scene_id"], inplace=True)
        return df_cat

    def _concat_df(self, change_df_list, columns):
        df_cat = pd.DataFrame(columns=columns)
        for df in change_df_list:
            data_dict = self.df_to_dict(df, None, lf='left')
            df_cat = df_cat.append(data_dict, ignore_index=True)
        return df_cat

    def _get_failure_model_df(self):
        if self.failure_df is None:
            from app.ctrl.ctrl_ds_drbfm import CtrlDSFailure
            # 获取着眼点
            self.failure_df = CtrlDSFailure().get_failure_df()
        return self.failure_df

    def _get_failure_df(self):
        if self.failure_df is None:
            from app.ctrl.ctrl_ds_drbfm import CtrlDSFailure
            # 获取着眼点
            self.failure_df = CtrlDSFailure().get_failure_df()
        return self.failure_df

    def _get_scene_df(self):
        if self.scene_df is None:
            from app.ctrl.ctrl_ds_scene import CtrlDSScene
            # 获取着眼点
            self.scene_df = CtrlDSScene().get_scene_df()
        return self.scene_df

    def df_to_dict(self, df1, df2=None, lf='left',
                   col_col=JournalDetail.column_name.name,
                   val_col=JournalDetail.val.name):
        """DataFrame 2 dict
        :param df1:
        :param df2:
        :param lf: left, right
        :param col_col: 字段
        :param val_col: 值
        :return:
        """
        d = dict()
        if df2 is None or df2.empty:
            for _, row in df1.iterrows():
                column_name = row[col_col]
                if column_name:
                    d[column_name] = row[val_col]
            if lf == 'left':
                d["action"] = 'delete'  # 删除
            else:
                d["action"] = 'add'  # 新增
            return d
        left_suffix = ''.join(['_', lf])
        # left_key_col = ''.join([JournalBrief.key_id.name, left_suffix])
        left_val_col = ''.join([JournalDetail.val.name, left_suffix])
        merge_df = pd.merge(df1, df2, how='left',
                            on=self.df_keys,
                            suffixes=('', left_suffix))
        # print(merge_df.columns)
        action = self._get_action(merge_df, left_val_col, lf)
        d["action"] = action
        merge_df.fillna(value='', inplace=True)
        for _, row in merge_df.iterrows():
            column_name = row[col_col]
            if column_name:
                val = row[val_col]
                # ID不添加颜色
                if((column_name.endswith('_id') and column_name != 'func_id')or
                   column_name.endswith('gid') or
                   column_name in ('sec_type', "micro_ver",
                                   "status", 'doc_type')):
                    d[column_name] = val
                    continue
                compare_val = row[left_val_col]
                d[column_name] = self._diff_and_set_color(val, compare_val, lf)
            else:
                current_app.logger.error('Unknown column_name.')
                pass
        return d

    def _get_action(self, merge_df, column, lf):
        # print(pd.notnull(merge_df[column]))
        if set(pd.notnull(merge_df[column])) == set([False]):  # 全空
            if lf == 'left':
                return 'delete'  # 删除
            else:
                return 'add'  # 新增
        return ''  # change/same


class CtrlSectionJournal(CtrlDSDocJournal):
    def __init__(self):
        CtrlDSDocJournal.__init__(self)
        self.table_name = 'ds_section'

    def df_to_dict(self, df1, df2=None, lf='left',
                   col_col=JournalDetail.column_name.name,
                   val_col=JournalDetail.val.name):
        """DataFrame 2 dict
        :param df1:
        :param df2:
        :param lf: left, right
        :param col_col: 字段
        :param val_col: 值
        :return:
        """
        d = dict()
        if df2 is None or df2.empty:
            for _, row in df1.iterrows():
                column_name = row[col_col]
                if column_name:
                    d[column_name] = row[val_col]
            return d
        left_suffix = ''.join(['_', lf])
        # left_key_col = ''.join([JournalBrief.key_id.name, left_suffix])
        left_val_col = ''.join([JournalDetail.val.name, left_suffix])
        merge_df = pd.merge(df1, df2, how='left',
                            on=self.df_keys,
                            suffixes=('', left_suffix))
        action = self._get_action(merge_df, left_val_col, lf)
        d["action"] = action
        merge_df.fillna(value='', inplace=True)
        for _, row in merge_df.iterrows():
            column_name = row[col_col]
            if column_name:
                val = row[val_col]
                # 不添加颜色
                if column_name not in ('sec_title', 'explain', 'complement'):
                    d[column_name] = val
                    continue
                compare_val = row[left_val_col]
                new_val = self._diff_and_set_color(val, compare_val, lf)
                d[column_name] = new_val
                # content
                # compare_val = row[left_val_col]
                # content1, content2, new_content = dict(), dict(), dict()
                # if val and val not in ('[]', 'null'):
                #     content1 = json.loads(val)[0]
                # if compare_val:
                #     content2 = json.loads(compare_val)[0]
                # for key, v1 in content1.items():
                #     if key in ("val", "title"):
                #         v2 = content2.get(key, '')
                #         new_val = self._diff_and_set_color(v1, v2, lf)
                #         new_content[key] = new_val
                #     else:
                #         new_content[key] = v1
                # d[column_name] = json.dumps([new_content])
            else:
                current_app.logger.error('Unknown column_name.')
                pass
        return d

    def cmp_content(self, content1, content2, lf='left'):
        new_content = dict()
        if not content1:
            return dict()
        content1 = json.loads(content1)[0]
        if content2:
            content2 = json.loads(content2)[0]
        else:
            content2 = dict()
        for key, v1 in content1.items():
            if key in ("val", "title"):
                v2 = content2.get(key, '')
                new_val = self._diff_and_set_color(v1, v2, lf)
                new_content[key] = new_val
            # else:
            #     new_content[key] = v1
        return new_content

