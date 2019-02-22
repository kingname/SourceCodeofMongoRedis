import redis

client = redis.Redis()

# 获取所有字段名
# field_names = client.hkeys('people_info')
# for name in field_names:
#     print(name.decode())

# 获取一条数据
# info = client.hget('people_info', '张小二')
# print(info.decode())
#
# # 获取多条数据
# info_list = client.hmget('people_info', ['王小三', '刘小五'])
# for info in info_list:
#     print(info.decode())
#
# # 获取所有字段名和值
# all_info = client.hgetall('people_info')
# print(all_info)


# 判断字段是否存在
# if client.hexists('people_info', '张小二'):
#     print('有张小二这个字段')
# else:
#     print('没有张小二这个字段')

field_num = client.hlen('people_info')
print(f'people_info哈希表中一个有{field_num}个字段')