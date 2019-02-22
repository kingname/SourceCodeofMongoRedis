import pymongo
import redis


client = redis.Redis()
db = pymongo.MongoClient().qa_system
question = db.question
answer = db.answer

# for row in question.find({}, {'_id': 1}):
#     _id = str(row['_id'])
#     client.zadd('qa_system:question:vote', _id, 0)

for row in answer.find({}, {'_id': 1, 'question_id': 1}):
    _id = row['_id']
    client.zadd('qa_system:answer:{}:vote'.format(row['question_id']), _id, 0)