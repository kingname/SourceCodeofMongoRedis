import pymongo


conn = pymongo.MongoClient('mongodb://kingname:kingnameisgenius@localhost/chapter_8')
handler = conn.chapter_8.one_by_one
total_data_num = handler.find().count()
print('chapter_8一共有：{}条数据'.format(total_data_num))
