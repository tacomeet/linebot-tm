from datetime import datetime
from database.database import db
from linebot.models import TemplateSendMessage


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String())
    session_type = db.Column(db.Integer())
    session_stage = db.Column(db.Integer())
    thread_ts_contact = db.Column(db.String())
    thread_ts_other = db.Column(db.String())
    question_msg = db.Column(db.String())
    answer_msg = db.Column(db.String())
    is_matched = db.Column(db.Boolean())
    last_question_id = db.Column(db.Integer())
    created_at = db.Column(db.DateTime(), default=datetime.now)
    session_start_timestamp = db.Column(db.DateTime())
    last_handled_timestamp = db.Column(db.DateTime())

    def __init__(self, id, name, session_type=None, session_stage=0):
        self.id = id
        self.name = name
        self.session_type = session_type
        self.session_stage = session_stage
        self.thread_ts_contact = None
        self.thread_ts_other = None
        self.question_msg = None
        self.is_matched = False
        self.last_question_id = None
        self.session_start_timestamp = None
        self.last_handled_timestamp = None

    def reset(self):
        self.answer_msg = None
        self.session_type = None
        self.session_stage = 0

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_session_stage(self):
        return self.session_stage

    def set_session_stage(self, session_stage):
        self.session_stage = session_stage

    def get_session_type(self):
        return self.session_type

    def set_session_type(self, session_type):
        self.session_type = session_type

    def increment_session_stage(self):
        self.session_stage += 1

    def get_thread_ts_contact(self):
        return self.thread_ts_contact

    def set_thread_ts_contact(self, thread_ts):
        self.thread_ts_contact = thread_ts

    def get_thread_ts_other(self):
        return self.thread_ts_other

    def set_thread_ts_other(self, thread_ts):
        self.thread_ts_other = thread_ts

    def get_question_msg(self):
        return self.question_msg

    def set_question_msg(self, question):
        if isinstance(question, list):
            self.question_msg = question[0]
            for q in question[1:]:
                if isinstance(q, str):
                    self.question_msg += '\n' + q
                elif isinstance(q, TemplateSendMessage):
                    self.question_msg += '\n' + q.alt_text
        elif isinstance(question, str):
            self.question_msg = question
        elif isinstance(question, TemplateSendMessage):
            self.question_msg = question.alt_text

    def get_answer_msg(self):
        return self.answer_msg

    def set_answer_msg(self, answer):
        if self.answer_msg is None:
            self.answer_msg = answer
        else:
            self.answer_msg += '\n' + answer

    def reset_answer_msg(self):
        self.answer_msg = None

    def get_is_matched(self):
        return self.is_matched

    def set_is_matched(self, is_matched):
        self.is_matched = is_matched

    def set_last_question_id(self, question_id):
        # question_id is either tag id or catcher id
        self.last_question_id = question_id

    def set_session_start_timestamp(self):
        self.session_start_timestamp = datetime.now()

    def get_session_start_timestamp(self):
        return self.session_start_timestamp

    def get_last_handled_timestamp(self):
        return self.last_handled_timestamp

    def set_last_handled_timestamp(self):
        self.last_handled_timestamp = datetime.now()
