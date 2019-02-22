import redis
import json

client = redis.Redis()
listener = client.pubsub(ignore_subscribe_messages=True)
listener.subscribe('computer', 'math', 'shopping')
for message in listener.listen():
    channel = message['channel'].decode()
    data = message['data'].decode()
    print(f'频道：{channel} 发了一条新信息：{data}')

