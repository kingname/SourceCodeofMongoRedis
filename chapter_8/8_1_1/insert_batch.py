import csv
import time
import pymongo

with open('people_info.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    people_info_list = [x for x in reader]

handler = pymongo.MongoClient().chapter_8.batch

start_time = time.time()
handler.insert_many(people_info_list)
end_time = time.time()
print('批量插入数据，耗时：', end_time - start_time)
