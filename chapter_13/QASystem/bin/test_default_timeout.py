import pymongo
from pymongo.collection import Collection
import time
handler = pymongo.MongoClient().chapter_13.test_data

# 生成数据
# data = []
# for i in range(200):
#     data.append({'data': i})
#
# handler.insert_many(data)

# 第一种方法：减少批量获取的条数
for data in handler.find().batch_size(80):
    print(f'这一行数据为：{data}')
    time.sleep(7)

# 第二种方法：设置游标用不超时
cursor = handler.find(no_cursor_timeout=True)
for data in cursor:
    print(f'这一行数据为：{data}')
    time.sleep(7)
cursor.close()
