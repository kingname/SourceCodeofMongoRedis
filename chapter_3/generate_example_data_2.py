from pymongo import MongoClient
client = MongoClient()
database= client.chapter_3
collection = database.example_data_2
collection.insert_many([
    {'name': '李大娃', 'age': 10, 'grade': '五年级', 'student': True, 'interest': '唱歌'},
    {'name': '张二娃', 'age': 12, 'grade': '六年级', 'student': True,  'interest': '跳舞'},
    {'name': '马三娃', 'age': 14, 'grade': '八年级', 'student': True,  'interest': '下棋'},
    {'name': '刘四娃', 'age': 16, 'grade': None, 'student': False,  'interest': '无'},
    {'name': '朱五娃', 'age': 18, 'grade': '高三', 'student': True,  'interest': '写字'},
    {'name': '高六娃', 'age': 8, 'grade': '一年级', 'student': True,  'interest': '学习'},
    {'name': '赵气娃', 'age': 10, 'grade': '五年级', 'student': True,  'interest': '乐高'},
    {'name': '葫芦娃', 'age': 100, 'grade': None, 'student': False,  'interest': '喷火'},
])