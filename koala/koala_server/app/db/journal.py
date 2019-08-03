
from ..db import db


class Journal(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = "journals"

    journalized_id = db.Column(db.INTEGER, primary_key=True)
    journalized_type = db.Column(db.String(30))
    user_id = db.Column(db.String(30))
    notes = db.Column(db.String)
    create_time = db.Column(db.Date)  # 创建时间


class JournalBrief(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = "journal_briefs"

    j_brief_id = db.Column(db.INTEGER, primary_key=True)
    journalized_id = db.Column(db.INTEGER, db.ForeignKey('public.journals.journalized_id'))
    key_id = db.Column(db.INTEGER)
    table_name = db.Column(db.String(100))
    action = db.Column(db.String(10))


class JournalDetail(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = "journal_details"

    j_detail_id = db.Column(db.INTEGER, primary_key=True)
    j_brief_id = db.Column(db.INTEGER, db.ForeignKey('public.journal_briefs.j_brief_id'))
    # key_id = db.Column(db.INTEGER)
    column_name = db.Column(db.String(100))
    val = db.Column(db.String)  # 值

