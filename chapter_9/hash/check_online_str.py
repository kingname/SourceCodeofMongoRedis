import redis

client = redis.Redis()


def set_online_status(user_id):
    """
    当用户登录网站的时候，调用这个函数，在Redis中设置一个字符串
    :param user_id: 用户账号
    :return: None
    """
    client.set(user_id, 1)


def set_offline_status(user_id):
    """
    当用户登出网站时调用这个函数，从Redis中删除这个以用户账号为Key的字符串
    :param user_id: 用户账号
    :return: None
    """
    client.delete(user_id)


def check_online_status(user_id):
    """
    检查用户是否在线，如果在线，那么get用户账号对应的Key就会返回1，否则返回None
    :param user_id: 用户账号
    :return: bool
    """
    online_status = client.get(user_id)
    if online_status and online_status.decode() == '1':
        return True
    return False