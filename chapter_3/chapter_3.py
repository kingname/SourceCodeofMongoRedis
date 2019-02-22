from pymongo import MongoClient
client = MongoClient()
database= client.chapter_3
collection = database.example_data_1
# rows = collection.find({'age': {'$lt': 25, '$gt': 21},
#                         'name': {'$ne': '夏侯小七'}})
# for row in rows:
#     print(row)

# result = collection.update_many(
#     {'name': '公孙小八'},
#     {'$set': {'address': '美国', 'age': 80}}
# )

# result = collection.update_one({'name': '隐身人'},
#                                {'$set': {'name': '隐身人',
#                                          'age': 0,
#                                          'address': '里世界'}},
#                                upsert=True)
# result = collection.delete_many({'age': 0})
# print(result)



