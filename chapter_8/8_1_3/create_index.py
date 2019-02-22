import time
import pymongo


start_time = time.time()
handler = pymongo.MongoClient().chapter_8.one_by_one
handler.create_index('salary', background=True)