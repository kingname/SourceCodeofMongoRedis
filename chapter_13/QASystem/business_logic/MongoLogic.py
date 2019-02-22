import datetime
from typing import List, Tuple
from bson import ObjectId
import config
from model import mongo_util

class MongoLogic(object):
    def __init__(self):
        self.question_name = config.QUESTION_COLLECTION
        self.answer_name = config.ANSWER_COLLECTION
        self.user_name = config.USER_COLLECTION
        self.vote_name = config.VOTE_COLLECTION
        self.mongo_util = mongo_util
        self.mongo_util.set_handler(self.question_name)
        self.mongo_util.set_handler(self.answer_name)
        self.mongo_util.set_handler(self.user_name)
        self.mongo_util.set_handler(self.vote_name)

    def insert_answer(self, question_id, answer, author, now):
        data_to_insert = {
            'author': author,
            'question_id': ObjectId(question_id),
            'answer': answer,
            'answer_time': now
        }
        object_id = str(self.mongo_util.insert_one(self.answer_name, data_to_insert))
        return object_id

    def insert_question(self, title, detail, author, now):
        data_to_insert = {
            'title': title,
            'detail': detail,
            'author': author,
            'ask_time': now
        }
        doc_id = self.mongo_util.insert_one(self.question_name, data_to_insert)
        return str(doc_id)

    def save_user_info(self, user, password_hash):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user_info = {'user': user, 'password_hash': password_hash, 'avatar': '', 'register_time': now}
        user_id = self.mongo_util.insert_one(self.user_name, user_info)
        return str(user_id)

    def get_user_info(self, user):
        user_info = self.mongo_util.find_one(self.user_name, {'user': user})
        if not user_info:
            return {'success': False, 'reason': '找不到用户名！'}
        return {'success': True, 'user_info': user_info}

    def update_question(self, question_id, title, text):
        result = self.mongo_util.update_one(self.question_name, {'_id': ObjectId(question_id)},
                                            {'$set': {'title': title, 'detail': text}})
        return result

    def update_answer(self, answer_id, text):
        self.mongo_util.update_one(self.answer_name, {'_id': ObjectId(answer_id)},
                                   {'$set': {'answer': text}})
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
        data = {'doc_type': doc_type,
                'doc_id': ObjectId(doc_id),
                'value': value,
                'user': user,
                'vote_time': vote_time
        }
        self.mongo_util.insert_one(self.vote_name, data)

    def query_question(self, question_id_score_list: List[Tuple[bytes, int]]) -> (dict, int):
        """
        根据问题ID和点赞数列表，查询问题
        :param question_id_score_list:
        :return:
        """
        total_question = self.mongo_util.find(self.question_name).count()
        id_score_dict = {}
        id_order_dict = {}
        object_id_list = []
        for index, question_id_score in enumerate(question_id_score_list):
            question_id = question_id_score[0].decode()
            score = int(question_id_score[1])
            id_score_dict[question_id] = score
            id_order_dict[question_id] = index
            object_id_list.append(ObjectId(question_id))
        question_iter_obj = self.mongo_util.aggregate(self.question_name, [
            {'$match': {'_id': {'$in': object_id_list}}},
            {'$lookup': {
             'from': 'answer',
             'localField': '_id',
             'foreignField': 'question_id',
             'as': 'answer_list'}}])

        question_list = []
        for question in question_iter_obj:
            question_list.append(
                {'title': question['title'],
                 'detail': question['detail'],
                 'author': question['author'],
                 'vote_up': id_score_dict[str(question['_id'])],
                 'answer_number': len(question['answer_list']),
                 'question_id': str(question['_id'])
                 }
            )
        question_list = sorted(question_list, key=lambda x: id_order_dict[x['question_id']])
        return question_list, total_question

    def query_answer(self, question_id: str, answer_id_score_list: List[Tuple[bytes, int]]) -> dict:
        """
        根据Redis中的获取到的答案列表，查询答案
        :param question_id: 问题ID
        :param answer_id_score_list: 答案ID和点赞数列表
        :return:
        """
        id_score_dict = {}
        id_order_dict = {}
        object_id_list = []
        for index, answer_id_score in enumerate(answer_id_score_list):
            answer_id = answer_id_score[0].decode()
            score = int(answer_id_score[1])
            id_score_dict[answer_id] = score
            id_order_dict[answer_id] = index
            object_id_list.append(ObjectId(answer_id))
        question = self.mongo_util.find_one(self.question_name, {'_id': ObjectId(question_id)})
        question_answer_dict = {
            'question_id': str(question['_id']),
            'question_title': question['title'],
            'question_detail': question['detail'].split('\n'),
            'question_author': question['author'],
            'answer_num': self.mongo_util.find(self.answer_name, {'question_id': ObjectId(question_id)}).count()
        }
        answers = self.mongo_util.find(self.answer_name, {'_id': {'$in': object_id_list}})
        answer_list = []
        for answer in answers:
            answer_list.append(
                {'answer_detail': answer['answer'].split('\n'),
                 'answer_author': answer['author'],
                 'answer_id': str(answer['_id']),
                 'answer_vote': id_score_dict[str(answer['_id'])]})
        answer_list = sorted(answer_list, key=lambda x: id_order_dict[x['answer_id']])
        question_answer_dict['answer_list'] = answer_list
        return question_answer_dict
