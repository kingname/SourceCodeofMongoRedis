import pymongo
import json
from bson import ObjectId

class MongoUtil(object):
    def __init__(self):
        db = pymongo.MongoClient().qa_system
        self.question = db.question
        self.answer = db.answer

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
            'question_detail': question_answer['detail'],
            'question_author': question_answer['author'],
            'answer_num': len(question_answer['answer_list'])
        }
        answer_list = []
        for answer in question_answer['answer_list']:
            answer_list.append(
                {'answer_detail': answer['answer'],
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
        self.question.insert_one(data_to_insert)
        return True

    def vote_for_question(self, object_id, value):
        self.question.update_one({'_id': ObjectId(object_id)}, {'$inc': {value: 1}})
        return True

    def vote_for_answer(self, object_id, value):
        self.answer.update_one({'_id': ObjectId(object_id)}, {'$inc': {value: 1}})
