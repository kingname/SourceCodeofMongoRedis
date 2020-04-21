from model import redis_util
import json
from typing import Generator, List, Tuple
from util.utils import login_expire


class RedisLogic(object):
    def __init__(self):
        self.redis_util = redis_util

    def save_session(self, session_id, session_info):
        session_json = json.dumps(session_info)
        self.redis_util.hash_set('qa_system:session', session_id, session_json)

    def delete_session(self, session_id):
        self.redis_util.delete_hash_field('qa_system:session', session_id)

    def fetch_session(self, session_id):
        if not session_id:
            return {}
        session_json = self.redis_util.hash_get('qa_system:session', session_id)
        if not session_json:
            return {}
        session_data = json.loads(session_json.decode())
        if login_expire(session_data=session_data):
            return {}
        return session_data

    def check_user_answer_question(self, user, question_id):
        return self.redis_util.is_hash_field_exists('qa_system:answer', user + question_id)

    def set_answer_flag(self, question, user):
        self.redis_util.hash_set('qa_system:answer', user+question, 1)

    def set_bit_value(self, offset_list: Generator) -> bool:
        """
        offset_list是一个生成器，需要使用for循环迭代它，每一次循环可以得到一个数字
        这个数字表示应该把Redis中名为qa_system:bloom的字符串的对应比特位设置为1
        :param offset_list: 生成器
        :return: bool
        """
        for offset in offset_list:
            self.redis_util.set_bit('qa_system:bloom', offset, 1)
        return True

    def is_all_bit_1(self, offset_list: Generator) -> bool:
        """
        检查Redis中，名为qa_system:bloom的字符串中，offset_list中每一个offset对应的位置的二进制值是否为1，
        一旦发现有1个不为1，就返回False, 只有全部offset对应的位置的二进制值全为1，才返回True
        :param offset_list: 生成器
        :return: bool
        """
        return self.redis_util.is_all_bit_1('qa_system:bloom', offset_list)

    def increase_vote_score(self, doc_type: str, doc_id: str, value: int, question_id: str='') -> bool:
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
        self.redis_util.increase_sorted_set_score(redis_key, doc_id, value)
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

        doc_id_score_list = self.redis_util.get_value_score_tuple_by_rank(redis_key, start, start + offset, withscores=True)
        return doc_id_score_list

    def add_question_vote_set(self, doc_id: str) -> None:
        """
        初始化问题的点赞数。问题添加完毕时，在Redis中，名为qa_system:question:vote的有序集合里初始化这个问题ID对应的评分为0
        :param doc_id: 问题ID
        :return:
        """
        redis_key = 'qa_system:question:vote'
        self.redis_util.sorted_set_add(redis_key, doc_id, 0)

    def add_answer_vote_set(self, question_id, answer_id):
        """
        初始化答案的点赞数。答案添加完成以后，在Redis中，名为qa_system:answer:<问题ID>:vote的有序集合中，
        初始化这个答案对应的点赞数为0
        :param question_id: 答案所属的问题的ID
        :param answer_id: 答案ID
        :return:
        """
        redis_key = 'qa_system:answer:{question_id}:vote'.format(question_id=question_id)
        self.redis_util.sorted_set_add(redis_key, answer_id, 0)

