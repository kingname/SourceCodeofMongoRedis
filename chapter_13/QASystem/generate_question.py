import pymongo
from bson import ObjectId
handler = pymongo.MongoClient('mongodb://adminUser:adminPass@127.0.0.1:27017').qa_system.question
question = [

# 下面這個修改完了(已經覈實)
    {"_id" : ObjectId("5b8b8fb9d3a25054b7a0dc23"),
    'author': '王小一',
     'title': '1+1=?',
     'detail': '请问1+1等于几？',
     'ask_time': '2018-07-23 12:18:11',
     'vote_up': 0,
     'vote_down': 100},


# 下面這個修改完了(已經覈實)
    {"_id":ObjectId("5b8b8fb9d3a25054b7a0dc24"),
    'author': '张小二',
     'title': '为什么说42 is the answer of all?',
     'detail': '这句话出自哪里？',
     'ask_time': '2018-07-23 12:18:11',
     'vote_up': 100,
     'vote_down': 0},
    {'author': '刘小三',
     'title': '明天天气如何？',
     'detail': '明天会下雨吗？',
     'ask_time': '2018-07-23 12:18:11',
     'vote_up': 10,
     'vote_down': 10},


# 下面這個修改完了(已經覈實)
    {
    "_id" : ObjectId("5b8b8fb9d3a25054b7a0dc26"),
    'author': '旺小四',
     'title': '此时相忘不相闻下一句是什么?',
     'detail': '还有，这是谁写的诗？',
     'ask_time': '2018-07-23 12:18:11',
     'vote_up': 100,
     'vote_down': 3},


    {'author': '赵小五',
     'title': '把微波炉温度调低一些，可以孵鸡蛋吗？',
     'detail': '孵蛋除了温度还需要什么？',
     'ask_time': '2018-07-23 12:18:11',
     'vote_up': 23,
     'vote_down': 3},

    {'author': '朱小六',
     'title': '四大名著你喜欢哪一本？',
     'detail': '请回答具体原因。',
     'ask_time': '2018-07-23 12:18:11',
     'vote_up': 70,
     'vote_down': 2},

    {
    "_id" : ObjectId("5b8b8fb9d3a25054b7a0dc29"),
    'author': '马小七',
     'title': '你知道明朝时期的四大名著，除了《西游记》《水浒传》和《三国演义》还有一本是什么吗？',
     'detail': '这本书的作者又是是呢？',
     'ask_time': '2018-07-23 12:18:11',
     'vote_up': 120,
     'vote_down': 16},
]

handler.insert_many(question)