import random
from pymongo import MongoClient

client = MongoClient().chapter_7.example_post2
name_list = ['衬衣', '裤子', '鞋子', '帽子']
size_list = ['S', 'M', 'L', 'XL']
price_list = [100, 200, 300, 600, 800]

for i in range(10):
    random_ = random.randint(2, 4)
    client.insert_one({
        'name': random.choice(name_list),
        'size': random.sample(size_list, random_),
        'price': random.sample(price_list, random_)
    })