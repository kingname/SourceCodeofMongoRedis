import time
import pymongo


start_time = time.time()
db = pymongo.MongoClient().chapter_8
batch = db.batch
new_collection = db.update_by_insert
new_people_info_list = []
for row in batch.find():
    salary = int(row['salary'])
    new_salary = salary + 100
    row['salary'] = str(new_salary)
    new_people_info_list.append(row)
new_collection.insert_many(new_people_info_list)
end_time = time.time()
print('使用插入代替更新，耗时：', end_time - start_time)

