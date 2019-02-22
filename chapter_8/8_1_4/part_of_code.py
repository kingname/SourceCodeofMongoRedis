def init():
    all_title = mongo_handler.distinct('title')
    redis_client.sadd('news_title', *all_title)


def need_insert_news(news_title):
    if redis_client.sadd('news_title', news_title) == 1:
        return True
    return False