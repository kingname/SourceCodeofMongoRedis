import pymongo
import redis


handler = pymongo.MongoClient('mongodb://root:iamsuperuser@localhost').chapter_9.rank_data
client = redis.Redis()

rows = handler.find({}, {'_id': 0})
for row in rows:
    client.zadd('rank', row['user_id'], row['score'])