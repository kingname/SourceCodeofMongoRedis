import redis

client = redis.Redis()

name = client.get('1000006')
print(f'ID为1000006的用户名是：{name.decode()}')
unknown_name = client.get('99999999')
print(f'如果查询的ID不存在，那么Redis返回：{unknown_name}')

# info = '''1000001 王小小
# 1000002 王大大
# 1000003 王小零
# 1000004 张小二
# 1000005 李小三
# 1000006 朱小四
# 1000007 刘小五
# 1000008 司马小六
# 1000009 慕容小七
# 1000010 夏侯小八'''
# for line in info.split('\n'):
#     _id = line.split(' ')[0]
#     name = line.split(' ')[1]
#     client.set(_id, name)

