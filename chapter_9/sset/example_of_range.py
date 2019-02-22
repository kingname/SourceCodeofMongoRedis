import redis


client = redis.Redis()

rank_100_1000 = client.zrange('rank', 0, 4, desc=True, withscores=True)
for index, one in enumerate(rank_100_1000):
    print(f'用户id： {one[0].decode()}, 积分：{one[1]}，排名第：{index + 1}')

client.zcount()