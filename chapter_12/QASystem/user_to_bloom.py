from answer.RedisUtil import RedisUtil
from util.BloomFilter import BloomFilter
import pymongo

users = ['kingname', '青南']
redis = RedisUtil()
bloom = BloomFilter(100000000, 0.001, redis)
bloom.set_key('青南')
x = bloom.check_duplicate('青南')
print(x)
# for user in users:
#     bloom.set_key(user)

