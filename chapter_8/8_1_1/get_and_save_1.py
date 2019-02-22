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
        if len(people_info_list) >= 1000:
            handler.insert_many(people_info_list)
            people_info_list = []
    else:
        break

if people_info_list:
    handler.insert_many(people_info_list)
