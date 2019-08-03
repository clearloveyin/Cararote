import time
import datetime
from app.db import db
from app.db.feature_func import CommonKey


class CtrlBase(object):
    def __init__(self):
        pass

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

    def get_common_key_id(self, type=None):
        new_cokey = CommonKey(type=type)
        db.session.add(new_cokey)
        db.session.flush()
        return new_cokey.key_id

