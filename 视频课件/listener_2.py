import redis
import time

client = redis.Redis()
chat = client.pubsub(ignore_subscribe_messages=True)
chat.subscribe('闲话2群')
while True:
    message = chat.get_message()
    if message:
        print(message['data'].decode())
    time.sleep(0.5)

