import time
import pymongo


start_time = time.time()
handler = pymongo.MongoClient().chapter_8.one_by_one
for row in handler.find({}, {'salary': 1}):
    salary = int(row['salary'])
    new_salary = salary + 100
    handler.update_one({'_id': row['_id']}, {'$set': {'salary': str(new_salary)}})
end_time = time.time()
print('逐条更新数据，耗时：', end_time - start_time)
