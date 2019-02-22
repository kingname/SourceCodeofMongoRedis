import pymongo
import datetime
from bson import ObjectId


class MongoUtil(object):
    def __init__(self):
        db = pymongo.MongoClient().qa_system
        self.question = db.question
        self.answer = db.answer
        self.user = db.user

    def query_question(self):
        question_iter_obj = self.question.aggregate([
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
                 'vote_up': question['vote_up'] - question['vote_down'],
                 'answer_number': len(question['answer_list']),
                 'question_id': str(question['_id'])
                 }
            )
        return question_list

    def query_answer(self, question_id):
        answer_iter_obj = self.question.aggregate([
            {'$match': {'_id': ObjectId(question_id)}},
            {'$lookup': {
                'from': 'answer',
                'localField': '_id',
                'foreignField': 'question_id',
                'as': 'answer_list'}}])
        question_answer = list(answer_iter_obj)[0]
        question_answer_dict = {
            'question_id': str(question_answer['_id']),
            'question_title': question_answer['title'],
            'question_detail': question_answer['detail'].split('\n'),
            'question_author': question_answer['author'],
            'answer_num': len(question_answer['answer_list'])
        }
        answer_list = []
        for answer in question_answer['answer_list']:
            answer_list.append(
                {'answer_detail': answer['answer'].split('\n'),
                 'answer_author': answer['author'],
                 'answer_id': str(answer['_id']),
                 'answer_vote': answer['vote_up'] - answer['vote_down']})
        question_answer_dict['answer_list'] = answer_list
        return question_answer_dict

    def insert_answer(self, question_id, answer, author, now, vote_up=0, vote_down=0):
        data_to_insert = {
            'author': author,
            'question_id': ObjectId(question_id),
            'answer': answer,
            'answer_time': now,
            'vote_up': vote_up,
            'vote_down': vote_down
        }
        self.answer.insert_one(data_to_insert)
        return True

    def insert_question(self, title, detail, author, now, vote_up=0, vote_down=0):
        data_to_insert = {
            'title': title,
            'detail': detail,
            'author': author,
            'ask_time': now,
            'vote_up': vote_up,
            'vote_down': vote_down
        }
        doc_id = self.question.insert_one(data_to_insert).inserted_id
        return str(doc_id)

    def vote_for_question(self, object_id, value):
        self.question.update_one({'_id': ObjectId(object_id)}, {'$inc': {value: 1}})
        return True

    def vote_for_answer(self, object_id, value):
        self.answer.update_one({'_id': ObjectId(object_id)}, {'$inc': {value: 1}})

    def save_user_info(self, user: str, password_hash: str) -> str:
        """
        保存用户信息，用于注册。
        :param user: 用户名
        :param password_hash: 经过加密的密码
        :return: 用户对应的ObjectId
        """
        return ''

    def get_user_info(self, user: str) -> dict:
        """
        根据用户名在MongoDB的user集合中查找用户的详细信息
        :param user: 用户名
        :return: 如果找不到用户名，返回的数据为：{'success': False, 'reason': '找不到用户名！'},
                 如果能够找到，返回的数据为{'success': True, 'user_info': user_info}，其中的
                user_info是一个字典，里面的数据是使用find_one查询到的值
        """

        return {'success': False, 'reason': '找不到用户名！'}

    def update_question(self, question_id: str, title: str, text: str) ->bool:
        """
        更新问题
        :param question_id: 问题对应的ObjectId
        :param title: 问题的标题
        :param text: 问题的详情
        :return: True or False
        """
        return True

    def update_answer(self, answer_id: str, text: str) -> bool:
        """
        更新回答
        :param answer_id: 答案对应的ObjectId
        :param text: 答案正文
        :return:
        """
        return True
