import random
from pymongo import MongoClient

client = MongoClient().chapter_7.example_post3
name_list = ['张三', '李四', '王五', '赵六']
date_list = ['2018/6/1', '2018/6/2', '2018/6/3', '2018/6/4']

for i in range(20):
    client.insert_one({
        '姓名': random.choice(name_list),
        '日期': random.choice(date_list),
        '分数': random.randint(50, 100)
    })
