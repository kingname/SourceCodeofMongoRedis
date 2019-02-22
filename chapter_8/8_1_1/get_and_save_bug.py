import redis
import json
import pymongo


client = redis.Redis()
handler = pymongo.MongoClient().chatper_8.people_info

people_info_list = []
while True:
    people_info_json = client.lpop('people_info')
    if people_info_json:
        people_info = json.loads(people_info_json.decode())
        people_info_list.append(people_info)
    else:
        break
handler.insert_many(people_info_list)
