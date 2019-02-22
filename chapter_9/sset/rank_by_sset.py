import redis

client = redis.Redis()

position = client.zrevrank('rank', 10017)
print(f'用户：10017排名为：{position + 1}')

rank = client.zrevrange('rank', 0, 10000, withscores=True)
print('从高到低排名如下：')
for index, one in enumerate(rank):
    print(f'用户id： {one[0].decode()}, 积分：{one[1]}，排名第：{index + 1}')


