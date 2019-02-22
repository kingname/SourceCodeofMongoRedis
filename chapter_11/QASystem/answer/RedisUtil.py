import redis
import json
from util.utils import login_expire


class RedisUtil(object):
    def __init__(self):
        self.client = redis.Redis()

    def check_user_registered(self, user):
        return self.client.sadd('qa_system:user:duplicate', user) == 0

    def save_session(self, session_id, session_info):
        session_json = json.dumps(session_info)
        self.client.hset('qa_system:session', session_id, session_json)

    def delete_session(self, session_id):
        self.client.hdel('qa_system:session', session_id)

    def fetch_session(self, session_id):
        if not session_id:
            return {}
        session_json = self.client.hget('qa_system:session', session_id)
        if not session_json:
            return {}
        session_data = json.loads(session_json.decode())
        if login_expire(session_data=session_data):
            return {}
        return session_data

    def check_user_answer_question(self, user, question_id):
        return self.client.hexists('qa_system:answer', user + question_id)

    def set_answer_flag(self, question, user):
        self.client.hset('qa_system:answer', user+question, 1)