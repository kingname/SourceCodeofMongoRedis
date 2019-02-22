import redis

client = redis.Redis()


def set_online_status(user_id):
    """
    当用户登录网站的时候，调用这个函数，在Redis中，名为user_online_status的哈希表中添加一个字段，字段名为用户账号，值为1
    :param user_id: 用户账号
    :return: None
    """
    client.hset('user_online_status', user_id, 1)


def set_offline_status(user_id):
    """
    当用户登出网站时调用这个函数，从Redis中名为user_online_status的哈希表中删除一个字段，字段名为用户账号
    :param user_id: 用户账号
    :return: None
    """
    client.hdel('user_online_status', user_id)


def check_online_status(user_id):
    """
    检查用户是否在线，如果哈希表user_online_status中以用户账号为名的字段，就返回True，否则返回False
    :param user_id: 用户账号
    :return: bool
    """
    return client.hexists('user_online_status', user_id)
