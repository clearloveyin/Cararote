# -*- coding: UTF-8 -*-
import time
import datetime
from app.db import db


class CtrlBase(object):

    def __init__(self):
        self.major_ver = 0
        self.minor_ver = 1
        self.micro_ver = 1

    def init_version(self, datainfo, type):
        if type == 'doc':
            datainfo['major_ver'] = self.major_ver
            datainfo['minor_ver'] = self.minor_ver
            datainfo['micro_ver'] = self.micro_ver
        elif type == 'section':
            datainfo['micro_ver'] = self.micro_ver
        return datainfo

    def update_version(self, ver):
        if ver:
            ver += 1
        else:
            ver = 1
        return ver

    def get_current_time(self):
        return time.strftime("%Y-%m-%d %H:%M:%S")

    def time_to_str(self, date_time):
        if type(date_time) in (datetime.datetime, datetime.time, datetime.date):
            date_time = date_time.strftime("%Y-%m-%d %H:%M:%S")
        return date_time

    def diff_ver(self, new_ver, old_ver):
        # return True, ''
        if new_ver == old_ver:
            return True, ''
        else:
            error = '已有人更新，请重新刷新页面！'
            return False, error

    def add_list(self, db_object, data_list, old_data_list, key_col, col_list):
        from app.ctrl.ctrl_diff import CtrlDiff
        diff_obj = CtrlDiff()
        match_list = diff_obj.match_list(old_data_list, data_list, key_col.name)
        log_list = []
        for match_dict in match_list:
            new_data = match_dict.get("new_data")
            old_data = match_dict.get("old_data")
            log_dict = self.common_add(db_object, new_data, old_data, col_list, key_col)
            if log_dict:
                log_list.append(log_dict)
        return log_list

    def common_add(self, db_object, new_data, old_data, col_list, key_col, diff_required=True):
        log_dict = dict()
        log_dict['table_name'] = db_object.__tablename__
        from app.ctrl.ctrl_diff import CtrlDiff
        diff_obj = CtrlDiff()
        if diff_required:
            action = diff_obj.diff_col(col_list, old_data, new_data)
        else:
            action = 'change'
        if action == 'same':
            return None
        elif action == 'add':
            if key_col.name in new_data:
                if not new_data[key_col.name]:
                    new_data.pop(key_col.name)
            new_obj = db_object(**new_data)
            db.session.add(new_obj)
            db.session.flush()
            key_id = new_obj.to_dict().get(key_col.name)
            log_dict['action'] = action
            log_dict['key_id'] = key_id
            log_dict['data'] = new_data
        elif action == 'change':
            key_id = new_data.get(key_col.name)
            db.session.query(db_object).filter(key_col == key_id).update(new_data)
            log_dict['action'] = action
            log_dict['key_id'] = key_id
            log_dict['data'] = new_data
        elif action == 'delete':
            key_id = old_data.get(key_col.name)
            db.session.query(db_object).filter(key_col == key_id).delete()
            log_dict['action'] = action
            log_dict['key_id'] = key_id
            log_dict['data'] = old_data
        return log_dict

    def commit_log(self, commit_list, commit_user, update_time):
        """
        把变更履历存进数据库
        :param commit_list:
        :param commit_user:
        :param update_time:
        :return: True:有变更/False:无变更
        """
        if commit_list:
            commit_log = dict()
            commit_log['commit_user'] = commit_user
            commit_log['update_time'] = update_time
            commit_log['commit_list'] = commit_list
            from app.ctrl.ctrl_journal import CtrlJournal
            CtrlJournal().add_journals(commit_log)

    def get_old_data(self, db_object, filter_col, key_id):
        q = db.session.query(db_object)
        if type(filter_col) == list:
            for col in filter_col:
                q = q.filter(col == key_id.get(col.name))
        else:
            q = q.filter(filter_col == key_id)
        data_list = []
        for data in q:
            data_list.append(data.to_dict())
        return data_list

    def db_query_to_list(self, querys):
        data_list = []
        for query in querys:
            data_list.append(query.to_dict())
        return data_list



