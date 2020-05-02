import redis
import pymongo


client = redis.Redis()
db = pymongo.MongoClient().qa_system
question_handler = db.question
answer_handler = db.answer


def generate_question_vote():
    for question in question_handler.find():
        doc_id = str(question['_id'])
        vote_up = question['vote_up']
        vote_down = question['vote_down']
        value = vote_up - vote_down
        client.zadd('qa_system:question:vote', {doc_id: value})


def generate_answer_vote():
    for answer in answer_handler.find():
        question_id = str(answer['question_id'])
        key = f'qa_system:answer:{question_id}:vote'
        vote_up = answer['vote_up']
        vote_down = answer['vote_down']
        value = vote_up - vote_down
        answer_id = str(answer['_id'])
        client.zadd(key, {answer_id: value})


generate_question_vote()
generate_answer_vote()
