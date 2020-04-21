import hashlib
from business_logic import RedisLogic
import math
from struct import unpack, pack


class BloomFilter(object):
    def __init__(self, capacity, error_rate):
        self.num_slices = int(math.ceil(math.log(1.0 / error_rate, 2)))
        self.bits_per_slice = int(math.ceil(
            (capacity * abs(math.log(error_rate))) /
            (self.num_slices * (math.log(2) ** 2))))
        self.hashs = self.make_hashfuncs(self.num_slices, self.bits_per_slice)
        self.redis_util = RedisLogic()

    def make_hashfuncs(self, num_slices, num_bits):
        """
        本函数修改自开源项目https://github.com/jaybaird/python-bloomfilter
        该项目基于MIT协议发布。对原开发者表示感谢。
        :param num_slices: 能够去重的数据量
        :param num_bits:  哈希函数的个数
        :return: 返回一个生成器，对生成器进行迭代可以得到所有需要置为1的二进制位的位置
        """
        if num_bits >= (1 << 31):
            fmt_code, chunk_size = 'Q', 8
        elif num_bits >= (1 << 15):
            fmt_code, chunk_size = 'I', 4
        else:
            fmt_code, chunk_size = 'H', 2
        total_hash_bits = 8 * num_slices * chunk_size
        if total_hash_bits > 384:
            hashfn = hashlib.sha512
        elif total_hash_bits > 256:
            hashfn = hashlib.sha384
        elif total_hash_bits > 160:
            hashfn = hashlib.sha256
        elif total_hash_bits > 128:
            hashfn = hashlib.sha1
        else:
            hashfn = hashlib.md5
        fmt = fmt_code * (hashfn().digest_size // chunk_size)
        num_salts, extra = divmod(num_slices, len(fmt))
        if extra:
            num_salts += 1
        salts = tuple(hashfn(hashfn(pack('I', i)).digest()) for i in range(num_salts))

        def _make_hashfuncs(key):
            if isinstance(key, str):
                key = key.encode('utf-8')
            else:
                key = str(key).encode('utf-8')
            i = 0
            for salt in salts:
                h = salt.copy()
                h.update(key)
                for uint in unpack(fmt, h.digest()):
                    yield uint % num_bits
                    i += 1
                    if i >= num_slices:
                        return

        return _make_hashfuncs

    def check_duplicate(self, key):
        offset_list = self.hashs(key)
        return self.redis_util.is_all_bit_1(offset_list)

    def set_key(self, key):
        offset_list = self.hashs(key)
        self.redis_util.set_bit_value(offset_list)




if __name__ == '__main__':
    bloom = BloomFilter(1000000000, 0.0001)
    a = bloom.make_hashfuncs(bloom.num_slices, bloom.bits_per_slice)
    print(list(a('test')))
