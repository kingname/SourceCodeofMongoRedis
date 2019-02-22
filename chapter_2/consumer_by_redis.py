import json
import time
import redis
import random
from threading import Thread
import re

re.S

class Consumer(Thread):
    def __init__(self):
        super().__init__()
        self.queue = redis.Redis()

    def run(self):
        while True:
            num_tuple = self.queue.blpop('producer')
            a, b = json.loads(num_tuple[1].decode())
            print(f'消费者消费了一组数，{a} + {b} = {a + b}')
            time.sleep(random.randint(0, 10))


consumer = Consumer()
consumer.start()
while True:
    time.sleep(1)
