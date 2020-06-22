import time
import random
from queue import Queue
from threading import Thread


class Producer(Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self):
        while True:
            a = random.randint(0, 10)
            b = random.randint(90, 100)
            print(f'生产者生产了两个数字：{a}, {b}')
            self.queue.put((a, b))
            time.sleep(2)


class Consumer(Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self):
        while True:
            num_tuple = self.queue.get(block=True)
            sum_a_b = sum(num_tuple)
            print(f'消费者消费了一组数，{num_tuple[0]} + {num_tuple[1]} = {sum_a_b}')
            time.sleep(random.randint(0, 10))


queue = Queue()
producer = Producer(queue)
consumer = Consumer(queue)

producer.start()
consumer.start()
while True:
    time.sleep(1)
