import redis
import json
from typing import Generator, List, Tuple
from util.utils import login_expire


class RedisUtil(object):
    def __init__(self):
        self.client = redis.Redis()

    def save_session(self, session_id, session_info):
        session_json = json.dumps(session_info)
        self.client.hset('qa_system:session', session_id, session_json)

    def delete_session(self, session_id):
        self.client.hdel('qa_system:session', session_id)

    def fetch_session(self, session_id):
        if not session_id:
            return {}
        session_json = self.client.hget('qa_system:session', session_id)
        if not session_json:
            return {}
        session_data = json.loads(session_json.decode())
        if login_expire(session_data=session_data):
            return {}
        return session_data

    def check_user_answer_question(self, user, question_id):
        return self.client.hexists('qa_system:answer', user + question_id)

    def set_answer_flag(self, question, user):
        self.client.hset('qa_system:answer', user+question, 1)

    def set_bit_value(self, offset_list: Generator) -> bool:
        """
        offset_list是一个生成器，需要使用for循环迭代它，每一次循环可以得到一个数字
        这个数字表示应该把Redis中名为qa_system:bloom的字符串的对应比特位设置为1
        :param offset_list: 生成器
        :return: bool
        """
        for offset in offset_list:
            self.client.setbit('qa_system:bloom', offset, 1)
        return True

    def is_all_bit_1(self, offset_list: Generator) -> bool:
        """
        检查Redis中，名为qa_system:bloom的字符串中，offset_list中每一个offset对应的位置的二进制值是否为1，
        一旦发现有1个不为1，就返回False, 只有全部offset对应的位置的二进制值全为1，才返回True
        :param offset_list: 生成器
        :return: bool
        """
        for offset in offset_list:
            if self.client.getbit('qa_system:bloom', offset) != 1:
                return False
        return True

    def set_string_if_not_exists(self, redis_key: str, value: int) -> bool:
        """
        使用Redis作为分布式锁。在设置字符串时，添加一个参数nx=True，如此一来，只有Redis
        不存在这个Key时才能创建成功并返回True。如果Redis中已经有这个Key了，那么就会返回
        None
        :param redis_key: 需要被设置的Key名
        :param value: 1
        :return: bool
        """
        if self.client.set(redis_key, value, nx=True):
            return True
        return False

    def delete_key(self, redis_key: str) -> bool:
        """
        从Redis中删除一个Key
        :param redis_key: Key名
        :return: bool
        """
        self.client.delete(redis_key)
        return True

    def increase_vote_score(self, doc_type: str, doc_id: str, value: str, question_id: str='') -> bool:
        """
        为问题或者回答点赞或者踩。对于问题，修改的是Redis中名为qa_system:question:vote的有序集合。对于回答，
        修改的是Redis中名为qa_system:answer:<问题ID>:vote的有序集合。这些有序集合的值是对应的问题ID或者回答
        ID，他们的Score是他们的赞同数。通过有序集合的zincrby方法，可以对score加1或者减1，从而实现修改赞同数的
        目的。
        :param doc_type: question或者answer
        :param doc_id: 问题ID或者回答ID
        :param value: 1或者-1
        :param question_id: 对于给回答点赞，需要知道这个答案是属于哪个问题的，所以还要问题ID
        :return: bool
        """
        if doc_type == 'question':
            redis_key = 'qa_system:{doc_type}:vote'.format(doc_type=doc_type)
        else:
            redis_key = 'qa_system:{doc_type}:{question_id}:vote'.format(doc_type=doc_type,
                                                                         question_id=question_id)
        self.client.zincrby(redis_key, doc_id, value)
        return True

    def get_doc_rank_range(self, doc_type: str, start: int, offset: int, question_id: str='') -> List[Tuple[bytes, int]]:
        """
        根据赞同数从高到低对问题或者回答进行排名，查询第start名到第start + offset名的问题或者答案。
        并把结果以如下格式返回：
        对于问题，返回
        [(问题ID1，问题1赞同数), (问题ID2, 问题2赞同数), ..., (问题IDn, 问题n赞同数)]
        对于答案，返回
        [(答案ID1，答案1赞同数), (答案ID2, 答案2赞同数), ..., (答案IDn, 问题n赞同数)]
        :param doc_type: question 或者 answer
        :param start: int
        :param offset: int
        :param question_id: 对于答案，需要知道这个答案是属于哪个问题的，所以还要问题ID
        :return:
        """
        if doc_type == 'question':
            redis_key = 'qa_system:{doc_type}:vote'.format(doc_type=doc_type)
        else:
            redis_key = 'qa_system:{doc_type}:{question_id}:vote'.format(doc_type=doc_type,
                                                                         question_id=question_id)

        doc_id_score_list = self.client.zrevrange(redis_key, start, start + offset, withscores=True)
        return doc_id_score_list

    def add_question_vote_set(self, doc_id: str) -> None:
        """
        初始化问题的点赞数。问题添加完毕时，在Redis中，名为qa_system:question:vote的有序集合里初始化这个问题ID对应的评分为0
        :param doc_id: 问题ID
        :return:
        """
        redis_key = 'qa_system:question:vote'
        self.client.zadd(redis_key, doc_id, 0)

    def add_answer_vote_set(self, question_id, answer_id):
        """
        初始化答案的点赞数。答案添加完成以后，在Redis中，名为qa_system:answer:<问题ID>:vote的有序集合中，
        初始化这个答案对应的点赞数为0
        :param question_id: 答案所属的问题的ID
        :param answer_id: 答案ID
        :return:
        """
        redis_key = 'qa_system:answer:{question_id}:vote'.format(question_id=question_id)
        self.client.zadd(redis_key, answer_id, 0)