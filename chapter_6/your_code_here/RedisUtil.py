import redis
import json
import hashlib


class RedisUtil(object):
    def __init__(self):
        self.chat_room_nick_set = 'chat_room_nick_set'
        self.cookie_nick = 'cookie-{}'
        self.chat_list = 'chat_list'

        # 你需要在这里初始化Redis
        self.client = redis.Redis()

    def is_nick_already_exists(self, nick):
        """
        你需要实现这个方法

        判断这个昵称是不是已经登录过了。如果已经登录，那么就不能使用这个昵称。
        使用Redis的集合实现，如果把昵称sadd到集合中返回1，说明这个昵称之前
        不存在，此时应该返回False，如果返回0，表示这个昵称之前已经存在了，此时应该返回True。

        :param nick: 昵称
        :return: True or False
        """
        is_flag = self.client.sadd(self.chat_room_nick_set, nick)
        if is_flag == 1:
            return False
        return True

    def set_token(self, nick, token):
        """
        你需要实现这个方法

        设定Token，这样的好处是只需要登录一次，以后可以直接访问/room页面直接进入聊天窗口
        使用Redis的字符串实现，字符串的Key是"cookie-昵称"，例如"cookie-青南"，值为参数token
        :param nick: 昵称
        :param token: md5字符串
        :return: None
        """
        key = self.cookie_nick.format(nick)
        self.client.set(key, token)

    def get_token(self, nick):
        """
        你需要实现这个方法

        获取Token，从"cookie-昵称"token并返回。

        使用Redis的字符串实现，字符串的Key为"cookie-昵称"，例如"cookie-青南"，如果这个Key存在，
        就获取它的值并返回，如果这个Key不存在，就返回None
        :param nick: 昵称
        :return: None 或者 Token字符串
        """
        key = self.cookie_nick.format(nick)
        token = self.client.get(key)
        return None if not token else token.decode()

    def get_chat_list(self):
        """
        你需要实现这个方法

        获取聊天消息列表。
        使用Redis的列表实现。Key为self.chat_list属性中保存的字符串，可以直接使用。
        获取列表右端20条信息，但不要删除。

        需要注意，从Redis中获取的数据一个列表，列表里面是bytes型的字符串，所以需要
        先把这个列表展开，把里面的bytes型的字符串解密为普通字符串以后再用json解析为
        字典。接下来讲解析出来的字典放入一个新的列表中。最后返回新的列表。
        :return: 包含字典的列表
        """
        chat_list = self.client.lrange(self.chat_list, -20, -1)
        chat_info_list = []
        for chat in chat_list:
            chat_info = json.loads(chat.decode())
            chat_info_list.append(chat_info)
        return chat_info_list

    def get_nick_msg_expire_time(self, nick, msg):
        """
        你需要实现这个方法

        获取某一个昵称发送某一条消息的过期时间。这个功能的作用是
        为了防止同一个用户短时间发送大量相同信息刷屏。

        为了防止信息太长，因此把信息编码为md5以后再与昵称拼接以缩短Key的长度。
        使用Redis的ttl命令来实现，ttl命令如果返回None，说明不存在这个Key，
        返回None。如果ttl返回-1，说明这个Key没有设定过期时间，这个Key可以一直存在
        如果ttl返回一个大于0的正整数，说明在这个整数对应的秒过于以后，Redis会自动
        删除这个Key

        :param nick: 昵称
        :param msg: 信息
        :return: None 或者 数字
        """
        msg_md5 = hashlib.md5(msg.encode()).hexdigest()
        duplicate_msg_check_flag = nick + msg_md5
        expire_time = self.client.ttl(duplicate_msg_check_flag)
        return expire_time

    def push_chat_info(self, chat_info):
        """
        你需要实现这个方法
        把聊天信息存入列表的右侧。
        使用Redis的集合实现，对应的Key为self.chat_list中保存的字符串。
        把chat_info字典先转化为JSON字符串，再存入Redis中列表中。

        为了防止列表消息太长，因此需要使用ltrim命令删除多余的信息，只保留
        列表最右侧的20条
        :param chat_info: 字典，格式为{'msg': '信息', 'nick': '青南', 'post_time': '2018-07-22 10:00:12'}
        :return: None
        """
        self.client.rpush(self.chat_list, json.dumps(chat_info))
        self.client.ltrim(self.chat_list, -20, -1)

    def set_nick_msg_expire_time(self, nick, msg):
        """
        你需要实现这个方法

        设定Key的过期时间，这个功能的目的是限定同一个用户在2分钟内不能发送同样的内容。
        为了防止信息太长，因此把信息编码为md5以后再与昵称拼接以缩短Key的长度。
        使用Redis的字符串实现，字符串的Key为昵称+信息的md5编码，值为1.使用set命令的
        ex参数设定Key的过期时间为120秒，时间到了以后Redis会自动删除这个Key
        :param nick: 昵称
        :param msg: 信息
        :return: None
        """
        msg_md5 = hashlib.md5(msg.encode()).hexdigest()
        duplicate_msg_check_flag = nick + msg_md5
        self.client.set(duplicate_msg_check_flag, 1, ex=120)
