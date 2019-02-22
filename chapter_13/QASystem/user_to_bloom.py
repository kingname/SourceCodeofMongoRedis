from model.RedisUtil import RedisLogic
from util.BloomFilter import BloomFilter

users = ['kingname', '青南']
redis = RedisLogic()
bloom = BloomFilter(100000000, 0.001, redis)
bloom.set_key('青南')
x = bloom.check_duplicate('青南')
print(x)
# for user in users:
#     bloom.set_key(user)

