import csv
import time
import pymongo

with open('people_info.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    people_info_list = [x for x in reader]

handler = pymongo.MongoClient().chapter_8.one_by_one

start_time = time.time()
for info in people_info_list:
    handler.insert_one(info)
end_time = time.time()

print('逐条插入数据，耗时：', end_time - start_time)
