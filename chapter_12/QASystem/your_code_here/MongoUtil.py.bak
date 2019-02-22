import pymongo
import datetime
from typing import List, Tuple
from bson import ObjectId


class MongoUtil(object):
    def __init__(self):
        db = pymongo.MongoClient().qa_system
        self.question = db.question
        self.answer = db.answer
        self.user = db.user
        self.vote = db.vote

    def insert_answer(self, question_id, answer, author, now):
        data_to_insert = {
            'author': author,
            'question_id': ObjectId(question_id),
            'answer': answer,
            'answer_time': now
        }
        object_id = str(self.answer.insert_one(data_to_insert).inserted_id)
        return object_id

    def insert_question(self, title, detail, author, now):
        data_to_insert = {
            'title': title,
            'detail': detail,
            'author': author,
            'ask_time': now
        }
        doc_id = self.question.insert_one(data_to_insert).inserted_id
        return str(doc_id)

    def vote_for_question(self, object_id, value):
        self.question.update_one({'_id': ObjectId(object_id)}, {'$inc': {value: 1}})
        return True

    def vote_for_answer(self, object_id, value):
        self.answer.update_one({'_id': ObjectId(object_id)}, {'$inc': {value: 1}})

    def save_user_info(self, user, password_hash):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user_info = {'user': user, 'password_hash': password_hash, 'avatar': '', 'register_time': now}
        user_id = self.user.insert_one(user_info).inserted_id
        return str(user_id)

    def get_user_info(self, user):
        user_info = self.user.find_one({'user': user})
        if not user_info:
            return {'success': False, 'reason': '找不到用户名！'}
        return {'success': True, 'user_info': user_info}

    def update_question(self, question_id, title, text):
        self.question.update_one({'_id': ObjectId(question_id)}, {'$set': {'title': title, 'detail': text}})
        return True

    def update_answer(self, answer_id, text):
        self.answer.update_one({'_id': ObjectId(answer_id)}, {'$set': {'answer': text}})
        return True

    def insert_vote(self, doc_type: str, doc_id: str, value: int, user: str, vote_time: str) -> None:
        """
        记录用户的点赞和踩的信息。
        :param doc_type: question或者answer
        :param doc_id:  问题ID或者答案ID
        :param value: 1 或者 -1
        :param user: 用户名
        :param vote_time: 插入时间
        :return:
        """
        return None

    def query_question(self, question_id_score_list: List[Tuple[bytes, int]]) -> (list, int):
        """
        根据问题ID和点赞数列表，查询问题
        :param question_id_score_list:
        :return:
        """
        return [], 0

    def query_answer(self, question_id: str, answer_id_score_list: List[Tuple[bytes, int]]) -> dict:
        """
        根据Redis中的获取到的答案列表，查询答案
        :param question_id: 问题ID
        :param answer_id_score_list: 答案ID和点赞数列表
        :return:
        """
        return {}
