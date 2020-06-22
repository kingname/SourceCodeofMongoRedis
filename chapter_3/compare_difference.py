from pymongo import MongoClient
from bson import ObjectId

client = MongoClient()
database = client.chapter_3
collection = database.example_data_2

# 1. 空值
# rows = collection.find({'grade': null})
rows = collection.find({'grade': None})

# 2. 布尔值
# rows = collection.find({'student': True}, {'_id': 0})

# 3. 排序参数
# rows = collection.find({}, {'_id': 0}).sort('age', -1)

# 4. 查询_id
# rows = collection.find({'_id': ObjectId('5b2f75d26b78a61364d09f45')},
#                        {'_id': 0})

for row in rows:
    print(row)