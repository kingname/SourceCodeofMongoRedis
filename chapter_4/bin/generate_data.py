import pymongo
import random
import datetime


handler = pymongo.MongoClient().chapter_4.people_info


last_name_list = '王，张，李，赵，朱，慕容，夏侯，诸葛，公孙，南宫，欧阳'.split('，')
first_name_list = '一，二，三，四，六，七，八，九，十，十一，十二，十三，十四，十五，十六，十七，十八，十九，二十'.split('，')
place_list = [
    '山东济南',
    '贵州贵阳',
    '广东广州',
    '河北邯郸',
    '四川成都',
    '湖北武汉',
    '北京',
    '天津',
    '陕西西安',
    '河南郑州'
]
data_list = []
for index, first_name in enumerate(first_name_list):
    age = random.randint(8, 30)
    this_year = datetime.date.today().year
    birthday = '{}-0{}-{}'.format(this_year - age,
                                  random.randint(1, 9),
                                  random.randint(10, 28))
    data = {'id': index + 1,
            'name': '{}{}{}'.format(random.choice(last_name_list),
                                    '' if len(first_name) == 2 else "小",
                                    first_name),
            'age': age,
            'birthday': birthday,
            'origin_home': random.choice(place_list),
            'current_home': random.choice(place_list),
            'deleted': 0}
    data_list.append(data)

print(data_list)
handler.insert_many(data_list)
