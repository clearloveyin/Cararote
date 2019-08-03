from flask import current_app
from app.db.issues import *
from app.db.users import Users
from app.ctrl.ctrl_base import CtrlBase
ISSUE_STATUS = ["打开", "已确认", "关闭"]


class CtrlIssue(CtrlBase):
    def __init__(self):
        CtrlBase.__init__(self)

    def add_issue(self, data):
        comment = data.get("comment")
        issue_user = data.get("issue_user")
        status = data.get("status")
        table_name = "func_man_day"
        key_id = data.get("base_id")
        commit_time = self.get_current_time()
        update_time = self.get_current_time()
        try:
            issue_info = {
                Issue.comment.name: comment,
                Issue.status.name: status,
                Issue.commit_time.name: commit_time,
                Issue.update_time.name: update_time,
                Issue.issue_user.name: issue_user,
                Issue.table_name.name: table_name,
                Issue.key_id.name: key_id,
            }
            issue = Issue(**issue_info)
            db.session.add(issue)
            db.session.commit()
            return True, ""
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"

    def update_issue_status(self, data_json):
        """修改指摘的状态"""
        issue_id = data_json.get("issue_id")
        status = data_json.get("status")
        issue_obj = db.session.query(Issue).filter(Issue.issue_id == issue_id).first()
        if issue_obj:
            issue_obj.status = status
            return True, ""
        else:
            return False, "该条指摘不存在！"

    def get_issue_list(self, base_id):
        issue_list = []
        q = db.session.query(Issue, Users.user_name).outerjoin(Users, Issue.issue_user == Users.user_id)
        if base_id:
            q = q.filter(Issue.key_id == base_id)
        q = q.order_by(Issue.issue_id)
        for q_obj in q:
            issue = dict()
            issue[Issue.issue_id.name] = q_obj.Issue.issue_id
            issue[Issue.comment.name] = q_obj.Issue.comment
            issue[Issue.commit_time.name] = self.time_to_str(q_obj.Issue.commit_time)
            # issue[Issue.update_time.name] = self.time_to_str(q_obj.update_time)
            issue[Issue.issue_user.name] = q_obj.user_name
            # issue[Issue.table_name.name] = q_obj.table_name
            # issue[Issue.key_id.name] = q_obj.key_id
            # issue[Issue.col_value.name] = q_obj.col_value
            issue[Issue.status.name] = q_obj.Issue.status
            issue_list.append(issue)
        return {"issue_list": issue_list, "status_list": ISSUE_STATUS}

    def add_replay(self, data):
        issue_id = data.get("issue_id")
        parent_replay_id = data.get("parent_replay_id")
        comment = data.get("comment")
        issue_user = data.get("issue_user")
        table_name = data.get("table_name")
        key_id = data.get("key_id")
        col_value = data.get("col_value")
        commit_time = self.get_current_time()
        update_time = self.get_current_time()
        try:
            pro_info = {
                Replay.issue_id.name: issue_id,
                Replay.parent_replay_id.name: parent_replay_id,
                Replay.comment.name: comment,
                Replay.status.name: 1,
                Replay.commit_time.name: commit_time,
                Replay.update_time.name: update_time,
                Replay.issue_user.name: issue_user,
                Replay.table_name.name: table_name,
                Replay.key_id.name: key_id,
                Replay.col_value.name: col_value,

            }
            pro = Replay(**pro_info)
            db.sesson.add(pro)
            db.sesson.commit()
            return pro.replay_id, ""
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"

    def get_replay_list(self):
        replay_list = []
        q = db.session.query(Replay).order_by(Replay.replay_id).all()
        for q_obj in q:
            replay = dict()
            replay[Replay.replay_id.name] = q_obj.replay_id
            replay[Replay.issue_id.name] = q_obj.issue_id
            replay[Replay.parent_replay_id.name] = q_obj.parent_replay_id
            replay[Replay.comment.name] = q_obj.comment
            replay[Replay.commit_time.name] = self.time_to_str(q_obj.commit_time)
            replay[Replay.update_time.name] = self.time_to_str(q_obj.update_time)
            replay[Replay.issue_user.name] = q_obj.issue_user
            replay[Replay.table_name.name] = q_obj.table_name
            replay[Replay.key_id.name] = q_obj.key_id
            replay[Replay.col_value.name] = q_obj.col_value
            replay_list.append(replay)
        return replay_list
