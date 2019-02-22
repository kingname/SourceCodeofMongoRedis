import pymongo
import random

handler = pymongo.MongoClient('mongodb://root:iamsuperuser@localhost').chapter_9.rank_data

for i in range(10000, 10100):
    data = {'user_id': i,
            'score': round(random.random() * 1000, 1)}
    handler.insert_one(data)