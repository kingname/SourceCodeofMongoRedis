import redis

user_num = 100
client = redis.Redis()


def use_string():
    for i in range(user_num):
        user_id = 10000 + i
        client.set(user_id, 1)


def use_hash():
    for i in range(user_num):
        user_id = 10000 + i
        client.hset('user_online_status', user_id, 1)


if __name__ == '__main__':
    use_hash()
