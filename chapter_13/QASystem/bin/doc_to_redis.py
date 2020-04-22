import pymongo
import redis

client = redis.Redis(password='appleyuchi',host='localhost', port=6379, db=0)
db = pymongo.MongoClient('mongodb://adminUser:adminPass@127.0.0.1:27017').qa_system
question = db.question
answer = db.answer

#----------------------------初始化问题数据集,写入redis-------------------------------------------------
# 先注释并且运行第一个for循环,
# {'_id': 1}表示mongodb查詢的結果中帶有_id
for row in question.find({}, {'_id': 1,'vote_up':1,'vote_down':1}):
    print("row=",row)
    _id = str(row['_id'])
    try:
        client.zadd('qa_system:question:vote', {_id:row['vote_up']-row['vote_down']})#所有問題的點讚數都是零
# 这里的_id指的是问题的value,0指的是点赞数(redis中的score)
    except:
    	client.zadd('qa_system:question:vote', {_id:0})#如果暫時沒有人對該問題點讚或者點踩，那麼點讚數設爲0

#----------------------------初始化答案数据集,写入redis-------------------------------------------------
for row in answer.find({}, {'_id': 1, 'question_id': 1,'vote_up':1,'vote_down':1}):
    _id = str(row['_id'])
    try:
        client.zadd('qa_system:answer:{}:vote'.format(str(row['question_id'])), {_id:row['vote_up']-row['vote_down']})
    except:
        client.zadd('qa_system:answer:{}:vote'.format(str(row['question_id'])), {_id:0})
