import redis
import time
import json

client = redis.Redis()
print('开始接收消息...')
last_message_time = None
while True:
    data = client.get('message')
    if not data:
        time.sleep(1)
        continue
    info = json.loads(data.decode())
    message = info['message']
    send_time = info['time']
    if send_time == last_message_time:
        #  这条信息已经接收过了，不需要重复接收
        time.sleep(1)
        continue
    print(f'接收到新信息：{message}, 发送时间为：{send_time}')
    last_message_time = send_time
