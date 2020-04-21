import redis
import config
from typing import Generator


class RedisUtil(object):
    def __init__(self):
        self.client = redis.Redis(host=config.REDIS_HOST,
                                  port=config.REDIS_PORT,
                                  password=config.REDIS_PASSWORD)

    def hash_set(self, key, field, value):
        self.client.hset(key, field, value)

    def delete_key(self, key):
        self.client.delete(key)

    def delete_hash_field(self, key, field):
        self.client.hdel(key, field)

    def hash_get(self, key, field):
        data = self.client.hget(key, field)
        return data

    def is_hash_field_exists(self, key, field):
        return self.client.hexists(key, field)

    def set_bit(self, key, offset, value):
        self.client.setbit(key, offset, value)

    def is_all_bit_1(self, key, offset_list: Generator) -> bool:
        for offset in offset_list:
            if not self.is_one_bit_1(key, offset):
                return False
        return True

    def is_one_bit_1(self, key, offset):
        return self.client.getbit(key, offset) == 1

    def set_string_if_not_exists(self, redis_key: str, value: int) -> bool:
        if self.client.set(redis_key, value, nx=True):
            return True
        return False

    def increase_sorted_set_score(self, key, target, value) -> bool:
        self.client.zincrby(key, value, target)
        return True

    def get_value_score_tuple_by_rank(self, key, rank_start, offset, withscores=True):
        doc_id_score_list = self.client.zrevrange(key, rank_start, rank_start + offset, withscores=withscores)
        return doc_id_score_list

    def sorted_set_add(self, key, value, score):
        self.client.zadd(key, {value: score})


redis_util = RedisUtil()
