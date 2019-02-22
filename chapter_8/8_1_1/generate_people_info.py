import csv
import random


first_word_in_name = '赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏水窦章云苏潘葛奚范彭郎'
second_word_in_name = '天地玄黄宇宙洪荒日月盈昃辰宿列张寒来暑往秋收冬藏闰余成岁律吕调阳云腾致雨露结为霜金生丽水玉出昆冈剑号巨阙'
third_word_in_name = '对酒当歌人生几何譬如朝露去日苦多慨当以慷忧思难忘何以解忧唯有杜康青青子衿悠悠我心但为君故沉吟至今'

work_number = 1
people_list = []
for first in first_word_in_name:
    for second in second_word_in_name:
        for third in third_word_in_name:
            name = first + second + third
            age = random.randint(0, 100)
            salary = random.randint(10000, 20000)
            phone_number = '1'
            for n in range(10):
                phone_number += str(random.randint(0, 9))
            people_list.append({'work_number': work_number,
                                'name': name,
                                'age': str(age),
                                'salary': str(salary),
                                'phone': phone_number})
            work_number += 1

with open('people_info.csv', 'w', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['work_number', 'name', 'age', 'salary', 'phone'])
    writer.writeheader()
    writer.writerows(people_list)