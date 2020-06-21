from pymongo import MongoClient

client = MongoClient()
database = client.chapter_3
collection = database.example_data_1

# 1. -------批量插入-------
# data_list = [
#     {'name': '朱小三', 'age': 20, 'address': '北京'},
#     {'name': '刘小四', 'age': 21, 'address': '上海'},
#     {'name': '马小五', 'age': 22, 'address': '山东'},
#     {'name': '夏侯小七', 'age': 23, 'address': '河北'},
#     {'name': '公孙小八', 'age': 24, 'address': '广州'},
#     {'name': '慕容小九', 'age': 25, 'address': '杭州'},
#     {'name': '欧阳小十', 'age': 26, 'address': '深圳'},
#
# ]
# collection.insert_many(data_list)

# 2. -------查询-------
rows = collection.find({})
# rows = collection.find({'age': {'$lt': 25, '$gt': 21},
#                         'name': {'$ne': '夏侯小七'}})
for row in rows:
    print(row)

# 3. -------更新-------
# result = collection.update_many(
#     {'name': '公孙小八'},
#     {'$set': {'address': '美国', 'age': 80}}
# )

# result = collection.update_one({'name': '隐身人'},
#                                {'$set': {'name': '隐身人',
#                                          'age': 0,
#                                          'address': '里世界'}},
#                                upsert=True)

# 4. -------删除-------
# result = collection.delete_many({'age': 0})
# print(result)
