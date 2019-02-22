import pymongo

handler = pymongo.MongoClient().chapter_7.example_post

weibo = [
    {'user_id': 1002, 'content': '考试完了，好无聊啊啊', 'post_time': '2018-06-11 12:23:12'},
    {'user_id': 1003, 'content': '大家看我今天吃得什么[图片]', 'post_time': '2018-06-11 12:27:12'},
    {'user_id': 1006, 'content': 'XX外卖送货太慢了，差评', 'post_time': '2018-06-11 14:00:12'},
    {'user_id': 1002, 'content': '我们不知道还能在一起多久', 'post_time': '2018-06-12 00:23:12'},
    {'user_id': 1001, 'content': '好不容易放假，楼上装修太吵了', 'post_time': '2018-06-12 08:23:12'},
    {'user_id': 1004, 'content': '疯了疯了疯了，我把洗衣服当成盐了', 'post_time': '2018-06-12 17:23:12'},
    {'user_id': 1004, 'content': '此处不留爷，自有留爷处', 'post_time': '2018-06-12 21:23:12'},
    {'user_id': 1005, 'content': '这个厕所设计得太美了', 'post_time': '2018-06-13 09:23:12'},
    {'user_id': 1007, 'content': 'XX叔，一路走好', 'post_time': '2018-06-13 17:23:12'},
    {'user_id': 1005, 'content': 'XX显示器的色彩太好看了', 'post_time': '2018-06-14 10:23:12'},
    {'user_id': 1008, 'content': '我在X市参与城市规划', 'post_time': '2018-06-15 12:01:12'},
    {'user_id': 1009, 'content': '小九中介竭诚为你服务', 'post_time': '2018-06-15 15:23:12'},
    {'user_id': 1001, 'content': '青山不改绿水长流，同学们后会有期', 'post_time': '2018-06-15 23:23:12'},
    {'user_id': 1003, 'content': '今天收到了小费。谢谢大老板。', 'post_time': '2018-06-15 23:23:12'},
         ]
handler.insert_many(weibo)
